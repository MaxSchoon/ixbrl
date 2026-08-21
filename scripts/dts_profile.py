#!/usr/bin/env python3
"""Walk a Discoverable Taxonomy Set and describe it.

A DTS is the closure of schemas and linkbases reachable from a starting
document through the discovery pointers XBRL 2.1 section 3.2 enumerates:
`link:schemaRef` and `link:linkbaseRef` in an instance, `xs:import` and
`xs:include` in a schema, `link:linkbaseRef` in a schema's appinfo,
`link:roleRef` / `link:arcroleRef`, and the `xlink:href` of every locator.
Every fact in a report binds to a concept declared somewhere in that closure,
and every label, reference, presentation parent, calculation weight and
dimension a concept carries is an edge in one of its linkbases. Reading the
DTS is therefore how you answer "which concept, which label, which network"
from evidence rather than from recall.

This script performs that walk with nothing but lxml, so it runs the same
offline as online, and reports two things:

  1. A structural PROFILE: documents by kind and host, concepts by
     substitution group / type / period / balance / abstractness, role types,
     presentation networks and their depth, calculation weights, XBRL
     Dimensions arcs, label roles and languages, reference parts, generic
     links and formula resources. Two taxonomies are compared by running it
     twice; see references/dts.md for the comparison it was built for.
  2. A CONCEPT view (`--concept`): the declaration, every label by role and
     language, every reference with its parts, and the concept's edges in
     each presentation, calculation and definition network.

Starting points accepted: an entry-point schema (`.xsd`, URL or path), an
xBRL-XML instance, an Inline XBRL document (its `ix:references`), or a
taxonomy / report package (`.zip` / `.xbri`: the package's
`META-INF/taxonomyPackage.xml` entry points, or the reports it contains).
`--package` registers further packages whose `META-INF/catalog.xml` rewrites
remote URIs to files inside the package, which is how a DTS resolves
offline (Taxonomy Packages 1.0 section 3.3).

What is deliberately NOT done here: XML Schema validation, XBRL 2.1
validation, arc prohibition / priority resolution beyond skipping
`use="prohibited"`, XDT validity, and formula evaluation. This is a reader
of the DTS, not a validator of it. Arelle validates; run it for a verdict.
The documents of the XBRL and W3C infrastructure namespaces (xbrl.org,
w3.org) are a boundary that is recorded, not followed, unless
`--follow-infrastructure` is given: they carry no reporting concepts and
would otherwise dominate every profile.

Usage:
  python dts_profile.py START [START ...] [--package PKG.zip ...]
                        [--cache-dir DIR] [--offline] [--json]
                        [--concept QNAME] [--follow-infrastructure]
                        [--max-documents N]

Exit codes: 0 = every discovered document resolved; 1 = profile produced but
at least one document or locator did not resolve (the report lists them, so
"OK" never overstates coverage); 2 = usage error or unreadable start;
127 = lxml missing.
"""

from __future__ import annotations

import argparse
import importlib
import json
import posixpath
import re
import shutil
import ssl
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    from lxml import etree
except ImportError:
    sys.stderr.write("This script requires lxml. Install: pip install lxml\n")
    sys.exit(127)

NS = {
    "xs": "http://www.w3.org/2001/XMLSchema",
    "link": "http://www.xbrl.org/2003/linkbase",
    "xlink": "http://www.w3.org/1999/xlink",
    "xbrli": "http://www.xbrl.org/2003/instance",
    "xbrldt": "http://xbrl.org/2005/xbrldt",
    "ix": "http://www.xbrl.org/2013/inlineXBRL",
    "gen": "http://xbrl.org/2008/generic",
    "tp": "http://xbrl.org/2016/taxonomy-package",
    "cat": "urn:oasis:names:tc:entity:xmlns:xml:catalog",
    "xml": "http://www.w3.org/XML/1998/namespace",
}

# Clark-notation forms for attribute access, derived from NS so the URI is
# declared once (CONTRIBUTING.md section Code conventions).
XLINK_HREF = f"{{{NS['xlink']}}}href"
XLINK_TYPE = f"{{{NS['xlink']}}}type"
XLINK_ROLE = f"{{{NS['xlink']}}}role"
XLINK_ARCROLE = f"{{{NS['xlink']}}}arcrole"
XLINK_LABEL = f"{{{NS['xlink']}}}label"
XLINK_FROM = f"{{{NS['xlink']}}}from"
XLINK_TO = f"{{{NS['xlink']}}}to"
XML_LANG = f"{{{NS['xml']}}}lang"
XBRLI_PERIOD_TYPE = f"{{{NS['xbrli']}}}periodType"
XBRLI_BALANCE = f"{{{NS['xbrli']}}}balance"
XBRLDT_TYPED_DOMAIN_REF = f"{{{NS['xbrldt']}}}typedDomainRef"

XS_SCHEMA = f"{{{NS['xs']}}}schema"
XS_ELEMENT = f"{{{NS['xs']}}}element"
XS_IMPORT = f"{{{NS['xs']}}}import"
XS_INCLUDE = f"{{{NS['xs']}}}include"
XS_REDEFINE = f"{{{NS['xs']}}}redefine"
LINK_LINKBASE = f"{{{NS['link']}}}linkbase"
LINK_LINKBASE_REF = f"{{{NS['link']}}}linkbaseRef"
LINK_SCHEMA_REF = f"{{{NS['link']}}}schemaRef"
LINK_ROLE_REF = f"{{{NS['link']}}}roleRef"
LINK_ARCROLE_REF = f"{{{NS['link']}}}arcroleRef"
LINK_ROLE_TYPE = f"{{{NS['link']}}}roleType"
LINK_ARCROLE_TYPE = f"{{{NS['link']}}}arcroleType"
LINK_USED_ON = f"{{{NS['link']}}}usedOn"
LINK_DEFINITION = f"{{{NS['link']}}}definition"
LINK_LABEL = f"{{{NS['link']}}}label"
LINK_REFERENCE = f"{{{NS['link']}}}reference"
XBRLI_XBRL = f"{{{NS['xbrli']}}}xbrl"
IX_REFERENCES = f"{{{NS['ix']}}}references"
TP_ENTRY_POINT_DOCUMENT = f"{{{NS['tp']}}}entryPointDocument"
CAT_REWRITE_URI = f"{{{NS['cat']}}}rewriteURI"

# Substitution-group roots that make a global element an XBRL concept
# (XBRL 2.1 section 5.1.1; XDT section 2.2 / 2.5). Taxonomies may interpose
# their own groups (the NT's `sbr:presentationItem`, for one), so membership is
# decided by walking the chain to one of these, never by the literal attribute.
CONCEPT_ROOTS = {
    f"{{{NS['xbrli']}}}item": "item",
    f"{{{NS['xbrli']}}}tuple": "tuple",
    f"{{{NS['xbrldt']}}}hypercubeItem": "hypercubeItem",
    f"{{{NS['xbrldt']}}}dimensionItem": "dimensionItem",
}

STANDARD_LABEL_ROLE = "http://www.xbrl.org/2003/role/label"
CONCEPT_LABEL_ARCROLE = "http://www.xbrl.org/2003/arcrole/concept-label"
CONCEPT_REFERENCE_ARCROLE = "http://www.xbrl.org/2003/arcrole/concept-reference"
PARENT_CHILD_ARCROLE = "http://www.xbrl.org/2003/arcrole/parent-child"
SUMMATION_ITEM_ARCROLES = {
    "http://www.xbrl.org/2003/arcrole/summation-item",
    "https://xbrl.org/2023/arcrole/summation-item",
}
XDT_ARCROLE_PREFIX = "http://xbrl.org/int/dim/arcrole/"

# Hosts whose documents are XBRL / W3C infrastructure (instance and linkbase
# schemas, XLink, XDT, the registries). Followed only on request.
INFRASTRUCTURE_HOSTS = {"www.xbrl.org", "xbrl.org", "www.w3.org"}

# Item-type local names bucketed by what they mean for tagging. Anything else is
# reported under its own local name, never folded into "other" silently.
TYPE_BUCKETS = {
    "monetaryItemType": "monetary",
    "sharesItemType": "shares",
    "pureItemType": "pure",
    "decimalItemType": "decimal",
    "integerItemType": "integer",
    "nonNegativeIntegerItemType": "integer",
    "percentItemType": "percent",
    "perShareItemType": "perShare",
    "areaItemType": "area",
    "volumeItemType": "volume",
    "energyItemType": "energy",
    "massItemType": "mass",
    "stringItemType": "string",
    "normalizedStringItemType": "string",
    "textBlockItemType": "textBlock",
    "escapedItemType": "textBlock",
    "dateItemType": "date",
    "dateTimeItemType": "date",
    "gYearItemType": "date",
    "gYearMonthItemType": "date",
    "durationItemType": "duration",
    "booleanItemType": "boolean",
    "domainItemType": "domain",
    "enumerationItemType": "enumeration",
    "enumerationSetItemType": "enumeration",
    "enumeration2ItemType": "enumeration",
    "enumerationSet2ItemType": "enumeration",
    "anyURIItemType": "anyURI",
    "QNameItemType": "QName",
}

USER_AGENT = "ixbrl-skill-dts-profile/1.0 (+https://doc2ixbrl.com)"
FETCH_TIMEOUT_SECONDS = 60
DEFAULT_MAX_DOCUMENTS = 5000


def secure_parser() -> etree.XMLParser:
    """An lxml parser hardened against XXE and entity expansion.

    Taxonomy files are fetched from the network, so they are untrusted input.
    Entity resolution and external DTD loading are disabled; `huge_tree` is
    enabled because the large label linkbases of the US-GAAP and IFRS
    taxonomies exceed lxml's default text-node limits and would otherwise be
    rejected as malformed.
    """
    return etree.XMLParser(
        recover=False,
        ns_clean=True,
        resolve_entities=False,
        no_network=True,
        load_dtd=False,
        huge_tree=True,
    )


def clark(qname: etree.QName | str) -> str:
    return str(qname)


def resolve_qname(el: etree._Element, value: str) -> str:
    """Expand a `prefix:local` attribute value against the element's scope."""
    prefix, sep, local = value.partition(":")
    if not sep:
        default = el.nsmap.get(None)
        return f"{{{default}}}{value}" if default else value
    ns = el.nsmap.get(prefix)
    return f"{{{ns}}}{local}" if ns else value


def split_clark(name: str) -> tuple[str, str]:
    if name.startswith("{"):
        ns, _, local = name[1:].partition("}")
        return ns, local
    return "", name


def is_url(value: str) -> bool:
    return value.startswith(("http://", "https://", "file://"))


def to_uri(start: str) -> str:
    """A start argument is a URL or a local path; local paths become file URIs."""
    if is_url(start):
        return start
    return Path(start).expanduser().resolve().as_uri()


def strip_fragment(uri: str) -> tuple[str, str]:
    base, _, fragment = uri.partition("#")
    return base, fragment


def join(base_uri: str, href: str) -> str:
    """Resolve a relative href against the document it appears in (RFC 3986)."""
    return urllib.parse.urljoin(base_uri, href)


def host_of(uri: str) -> str:
    parsed = urllib.parse.urlparse(uri)
    return parsed.netloc if parsed.scheme in ("http", "https") else "(local)"


class Catalog:
    """The `rewriteURI` entries of one or more taxonomy-package catalogs.

    Taxonomy Packages 1.0 restricts the OASIS XML Catalog to `rewriteURI`, and
    the longest matching `uriStartString` wins (XML Catalogs 1.1 section 7.2.2),
    which is what lets a package remap an entire namespace directory while a
    second, longer entry carves out one subdirectory.
    """

    def __init__(self) -> None:
        self.entries: list[tuple[str, str]] = []

    def load(self, catalog_path: Path) -> int:
        tree = etree.parse(str(catalog_path), secure_parser())
        base = catalog_path.resolve().as_uri()
        added = 0
        for entry in tree.getroot().iter(CAT_REWRITE_URI):
            start = entry.get("uriStartString")
            prefix = entry.get("rewritePrefix")
            if not start or not prefix:
                continue
            self.entries.append((start, join(base, prefix)))
            added += 1
        self.entries.sort(key=lambda item: len(item[0]), reverse=True)
        return added

    def rewrite(self, uri: str) -> str:
        for start, prefix in self.entries:
            if uri.startswith(start):
                return prefix + uri[len(start) :]
        return uri


def ssl_context() -> ssl.SSLContext:
    """The default TLS context, with certifi's bundle when the interpreter
    ships none (python.org macOS builds until their certificate script runs).
    """
    context = ssl.create_default_context()
    try:
        certifi = importlib.import_module("certifi")
    except ImportError:
        return context
    context.load_verify_locations(cafile=certifi.where())
    return context


class Fetcher:
    """Reads a document by URI: local file, or HTTP(S) through a disk cache.

    The cache mirrors the URL path under `cache_dir/host/`, so a second run,
    or an `--offline` run, reads the same bytes the first run did. A DTS
    profile is only reproducible with the inputs that produced it, and the
    cache is one of those inputs; say which directory you used when you cite
    a number from this tool.
    """

    def __init__(self, cache_dir: Path | None, offline: bool) -> None:
        self.cache_dir = cache_dir
        self.offline = offline
        self.network_fetches = 0
        self.cache_hits = 0

    def cache_path(self, uri: str) -> Path | None:
        if self.cache_dir is None:
            return None
        parsed = urllib.parse.urlparse(uri)
        path = parsed.path or "/"
        if path.endswith("/"):
            path += "index"
        # Normalise away any "..": a hostile href must not escape the cache root.
        safe = posixpath.normpath(path).lstrip("/")
        return self.cache_dir / parsed.netloc / safe

    def read(self, uri: str) -> tuple[bytes | None, str]:
        """Return (bytes, source) or (None, reason)."""
        parsed = urllib.parse.urlparse(uri)
        if parsed.scheme == "file":
            path = Path(urllib.request.url2pathname(parsed.path))
            if not path.is_file():
                return None, f"no such file: {path}"
            return path.read_bytes(), "file"
        if parsed.scheme not in ("http", "https"):
            return None, f"unsupported URI scheme: {parsed.scheme or '(none)'}"
        cached = self.cache_path(uri)
        if cached is not None and cached.is_file():
            self.cache_hits += 1
            return cached.read_bytes(), "cache"
        if self.offline:
            return None, "offline and not in cache"
        request = urllib.request.Request(uri, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(
                request, timeout=FETCH_TIMEOUT_SECONDS, context=ssl_context()
            ) as r:
                data = r.read()
        except urllib.error.HTTPError as exc:
            return None, f"HTTP {exc.code}"
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            reason = f"fetch failed: {exc}"
            if "CERTIFICATE_VERIFY_FAILED" in reason:
                reason += (
                    " (this Python has no CA bundle: pip install certifi, or set "
                    "SSL_CERT_FILE to a PEM bundle, or pass --package / --offline)"
                )
            return None, reason
        self.network_fetches += 1
        if cached is not None:
            cached.parent.mkdir(parents=True, exist_ok=True)
            cached.write_bytes(data)
        return data, "network"


@dataclass
class Concept:
    qname: str
    doc: str
    id: str | None
    type: str | None
    substitution_group: str | None
    abstract: bool
    nillable: bool
    period_type: str | None
    balance: str | None
    typed_domain_ref: str | None
    root: str | None = None  # item / tuple / hypercubeItem / dimensionItem

    @property
    def type_bucket(self) -> str:
        if self.type is None:
            return "(untyped)"
        _, local = split_clark(self.type)
        return TYPE_BUCKETS.get(local, local)


@dataclass
class Arc:
    linkbase: str  # presentation / calculation / definition / label / reference / other
    elr: str
    arcrole: str
    source: str  # concept QName, or "?" when the locator did not resolve
    target: str  # concept QName or resource key
    attrs: dict[str, str] = field(default_factory=dict)


@dataclass
class Document:
    uri: str
    kind: str  # schema / linkbase / instance / inline / package-manifest / other
    root: str
    target_namespace: str | None = None
    source: str = ""  # file / cache / network


@dataclass
class DTS:
    starts: list[str]
    documents: dict[str, Document] = field(default_factory=dict)
    unresolved: dict[str, str] = field(default_factory=dict)
    boundary: set[str] = field(default_factory=set)
    discovery: list[tuple[str, str, str]] = field(default_factory=list)
    concepts: dict[str, Concept] = field(default_factory=dict)
    ids: dict[tuple[str, str], str] = field(default_factory=dict)
    role_types: dict[str, dict[str, Any]] = field(default_factory=dict)
    arcrole_types: dict[str, dict[str, Any]] = field(default_factory=dict)
    arcs: list[Arc] = field(default_factory=list)
    labels: dict[str, list[tuple[str, str, str]]] = field(
        default_factory=lambda: defaultdict(list)
    )
    references: dict[str, list[dict[str, str]]] = field(
        default_factory=lambda: defaultdict(list)
    )
    generic_links: Counter[str] = field(default_factory=Counter)
    resources_by_kind: Counter[str] = field(default_factory=Counter)
    unresolved_locators: int = 0
    # Locators whose href names no concept in the closure, by what they point
    # at: a role/arcrole type or another non-concept id (legitimate: generic
    # labels on ELRs), a document outside the closure (a boundary or
    # unresolved document), or an id nothing declares.
    unresolved_locator_kinds: Counter[str] = field(default_factory=Counter)
    unresolved_locator_docs: Counter[str] = field(default_factory=Counter)
    prefixes: dict[str, str] = field(default_factory=dict)


class Walker:
    def __init__(
        self,
        fetcher: Fetcher,
        catalog: Catalog,
        follow_infrastructure: bool,
        max_documents: int,
    ) -> None:
        self.fetcher = fetcher
        self.catalog = catalog
        self.follow_infrastructure = follow_infrastructure
        self.max_documents = max_documents
        self.trees: dict[str, etree._Element] = {}

    # ── phase 1: discovery ────────────────────────────────────────────────

    def discover(self, starts: list[str]) -> DTS:
        dts = DTS(starts=list(starts))
        queue: list[tuple[str, str, str]] = [("(start)", "start", s) for s in starts]
        while queue:
            origin, pointer, uri = queue.pop(0)
            # Documents are keyed by their CANONICAL URI (the one the href
            # names). A package catalog only changes where the bytes are read
            # from; it must not change a document's identity, or the same
            # schema reached once via the catalog and once directly would be
            # counted twice and every host would read as local.
            uri, _ = strip_fragment(uri)
            if uri in dts.documents or uri in dts.unresolved or uri in dts.boundary:
                continue
            if not self.follow_infrastructure and host_of(uri) in INFRASTRUCTURE_HOSTS:
                dts.boundary.add(uri)
                dts.discovery.append((origin, pointer, uri))
                continue
            if len(dts.documents) >= self.max_documents:
                dts.unresolved[uri] = (
                    f"not fetched: --max-documents {self.max_documents}"
                )
                continue
            physical = self.catalog.rewrite(uri)
            data, source = self.fetcher.read(physical)
            if physical != uri:
                source = f"package ({source})"
            dts.discovery.append((origin, pointer, uri))
            if data is None:
                dts.unresolved[uri] = source
                continue
            try:
                root = etree.fromstring(data, secure_parser(), base_url=uri)
            except etree.XMLSyntaxError as exc:
                dts.unresolved[uri] = f"not well-formed XML: {exc}"
                continue
            doc = Document(
                uri=uri, kind=self.classify(root), root=root.tag, source=source
            )
            if doc.kind == "schema":
                doc.target_namespace = root.get("targetNamespace")
            dts.documents[uri] = doc
            self.trees[uri] = root
            for kind, href in self.pointers(root, doc.kind):
                queue.append((uri, kind, join(uri, href)))
        self.extract(dts)
        return dts

    @staticmethod
    def classify(root: etree._Element) -> str:
        tag = root.tag
        if tag == XS_SCHEMA:
            return "schema"
        if tag == LINK_LINKBASE:
            return "linkbase"
        if tag == XBRLI_XBRL:
            return "instance"
        if root.find(f".//{IX_REFERENCES}") is not None:
            return "inline"
        return "other"

    @staticmethod
    def pointers(root: etree._Element, kind: str) -> list[tuple[str, str]]:
        """The discovery pointers of one document, in document order.

        Schema: xs:import / xs:include / xs:redefine @schemaLocation, and the
        link:linkbaseRef, link:roleRef, link:arcroleRef inside xs:appinfo
        (XBRL 2.1 sections 3.2, 5.1.2). A typed dimension's
        xbrldt:typedDomainRef points at an element declaration that must be in
        the DTS (XDT section 2.5.2), so it is followed too.
        Linkbase: every locator href, plus roleRef / arcroleRef (3.2, 3.5.2.4).
        Instance and Inline XBRL: schemaRef / linkbaseRef / roleRef /
        arcroleRef, plus footnote locators (4.2, 4.3).
        """
        found: list[tuple[str, str]] = []
        if kind == "schema":
            for el in root.iter(XS_IMPORT, XS_INCLUDE, XS_REDEFINE):
                loc = el.get("schemaLocation")
                if loc:
                    found.append((etree.QName(el).localname, loc))
            for el in root.iter(LINK_LINKBASE_REF, LINK_ROLE_REF, LINK_ARCROLE_REF):
                href = el.get(XLINK_HREF)
                if href:
                    found.append((etree.QName(el).localname, href))
            for el in root.iter(XS_ELEMENT):
                ref = el.get(XBRLDT_TYPED_DOMAIN_REF)
                if ref:
                    found.append(("typedDomainRef", ref))
            return found
        for el in root.iter():
            if el.get(XLINK_TYPE) == "locator" or el.tag in (
                LINK_SCHEMA_REF,
                LINK_LINKBASE_REF,
                LINK_ROLE_REF,
                LINK_ARCROLE_REF,
            ):
                href = el.get(XLINK_HREF)
                if href:
                    local = etree.QName(el).localname
                    found.append(
                        (local if el.tag != LINK_LINKBASE_REF else "linkbaseRef", href)
                    )
        return found

    # ── phase 2: extraction ───────────────────────────────────────────────

    def extract(self, dts: DTS) -> None:
        for uri, root in self.trees.items():
            if dts.documents[uri].kind == "schema":
                self.extract_schema(dts, uri, root)
        self.resolve_substitution_groups(dts)
        for uri, root in self.trees.items():
            if dts.documents[uri].kind in ("linkbase", "instance", "inline"):
                self.extract_links(dts, uri, root)

    def extract_schema(self, dts: DTS, uri: str, root: etree._Element) -> None:
        tns = root.get("targetNamespace")
        for prefix, ns in root.nsmap.items():
            if prefix and tns and ns == tns and tns not in dts.prefixes:
                dts.prefixes[tns] = prefix
        for el in root.iter():
            el_id = el.get("id")
            if el_id:
                dts.ids[(uri, el_id)] = ""  # filled below for elements
        for el in root.findall(XS_ELEMENT):  # global declarations only
            name = el.get("name")
            if not name:
                continue
            qname = f"{{{tns}}}{name}" if tns else name
            el_id = el.get("id")
            type_attr = el.get("type")
            sg = el.get("substitutionGroup")
            concept = Concept(
                qname=qname,
                doc=uri,
                id=el_id,
                type=resolve_qname(el, type_attr) if type_attr else None,
                substitution_group=resolve_qname(el, sg) if sg else None,
                abstract=el.get("abstract", "false") == "true",
                nillable=el.get("nillable", "false") == "true",
                period_type=el.get(XBRLI_PERIOD_TYPE),
                balance=el.get(XBRLI_BALANCE),
                typed_domain_ref=el.get(XBRLDT_TYPED_DOMAIN_REF),
            )
            dts.concepts[qname] = concept
            if el_id:
                dts.ids[(uri, el_id)] = qname
        for rt in root.iter(LINK_ROLE_TYPE):
            role_uri = rt.get("roleURI")
            if role_uri:
                definition = rt.find(LINK_DEFINITION)
                dts.role_types[role_uri] = {
                    "doc": uri,
                    "definition": (definition.text or "").strip()
                    if definition is not None
                    else "",
                    "usedOn": [
                        (u.text or "").strip() for u in rt.findall(LINK_USED_ON)
                    ],
                }
        for at in root.iter(LINK_ARCROLE_TYPE):
            arcrole_uri = at.get("arcroleURI")
            if arcrole_uri:
                dts.arcrole_types[arcrole_uri] = {
                    "doc": uri,
                    "cyclesAllowed": at.get("cyclesAllowed"),
                    "usedOn": [
                        (u.text or "").strip() for u in at.findall(LINK_USED_ON)
                    ],
                }

    @staticmethod
    def resolve_substitution_groups(dts: DTS) -> None:
        """Walk each element's substitutionGroup chain to an XBRL root.

        Elements whose chain never reaches xbrli:item, xbrli:tuple or an XDT
        root are not concepts (schema-internal helpers, or declarations in a
        schema outside the closure) and are dropped from the concept set, with
        a count kept so the drop is visible.
        """
        resolved: dict[str, str | None] = {}
        for qname, concept in dts.concepts.items():
            chain: list[str] = []
            current: str | None = concept.substitution_group
            root: str | None = None
            while current is not None and current not in chain:
                if current in CONCEPT_ROOTS:
                    root = CONCEPT_ROOTS[current]
                    break
                chain.append(current)
                parent = dts.concepts.get(current)
                current = parent.substitution_group if parent else None
            resolved[qname] = root
        for qname, root in resolved.items():
            if root is None:
                del dts.concepts[qname]
            else:
                dts.concepts[qname].root = root

    def locator_target(self, dts: DTS, base_uri: str, href: str) -> str | None:
        doc_uri, fragment = strip_fragment(join(base_uri, href))
        m = re.fullmatch(r"element\((\S+)\)", fragment)
        if m and "/" not in m.group(1):
            fragment = m.group(1)
        qname = dts.ids.get((doc_uri, fragment))
        if qname:
            return qname
        if (doc_uri, fragment) in dts.ids:
            kind = "non-concept id (roleType, arcroleType, type, ...)"
        elif doc_uri in dts.boundary:
            kind = "document on the infrastructure boundary (not followed)"
        elif doc_uri in dts.unresolved:
            kind = "document unresolved"
        elif doc_uri not in dts.documents:
            kind = "document not in the closure"
        else:
            kind = "id not declared in that document"
        dts.unresolved_locator_kinds[kind] += 1
        dts.unresolved_locator_docs[doc_uri] += 1
        return None

    def extract_links(self, dts: DTS, uri: str, root: etree._Element) -> None:
        for ext in root.iter():
            if ext.get(XLINK_TYPE) != "extended":
                continue
            elr = ext.get(XLINK_ROLE, "")
            ext_ns, ext_local = split_clark(ext.tag)
            if ext_ns != NS["link"]:
                dts.generic_links[f"{ext_ns}#{ext_local}"] += 1
            linkbase = {
                "presentationLink": "presentation",
                "calculationLink": "calculation",
                "definitionLink": "definition",
                "labelLink": "label",
                "referenceLink": "reference",
                "footnoteLink": "footnote",
            }.get(ext_local, "other")
            locs: dict[str, list[str]] = defaultdict(list)
            resources: dict[str, list[etree._Element]] = defaultdict(list)
            arcs: list[etree._Element] = []
            for child in ext:
                xtype = child.get(XLINK_TYPE)
                label = child.get(XLINK_LABEL)
                if xtype == "locator" and label:
                    href = child.get(XLINK_HREF) or ""
                    target = self.locator_target(dts, uri, href)
                    if target is None:
                        dts.unresolved_locators += 1
                        target = "?"
                    locs[label].append(target)
                elif xtype == "resource" and label:
                    resources[label].append(child)
                    r_ns, r_local = split_clark(child.tag)
                    dts.resources_by_kind[f"{r_ns}#{r_local}"] += 1
                elif xtype == "arc":
                    arcs.append(child)
            for arc in arcs:
                arcrole = arc.get(XLINK_ARCROLE, "")
                from_label = arc.get(XLINK_FROM, "")
                to_label = arc.get(XLINK_TO, "")
                attrs = {
                    str(k): str(v)
                    for k, v in arc.attrib.items()
                    if k in ("order", "weight", "preferredLabel", "use", "priority")
                }
                for source in locs.get(from_label, ["?"]):
                    if to_label in resources:
                        for res in resources[to_label]:
                            self.record_resource(
                                dts, source, arcrole, res, linkbase, elr, attrs
                            )
                    for target in locs.get(to_label, []):
                        dts.arcs.append(
                            Arc(linkbase, elr, arcrole, source, target, attrs)
                        )

    @staticmethod
    def record_resource(
        dts: DTS,
        source: str,
        arcrole: str,
        res: etree._Element,
        linkbase: str,
        elr: str,
        attrs: dict[str, str],
    ) -> None:
        role = res.get(XLINK_ROLE, "")
        if res.tag == LINK_LABEL or arcrole == CONCEPT_LABEL_ARCROLE:
            lang = res.get(XML_LANG, "")
            text = " ".join("".join(str(t) for t in res.itertext()).split())
            if source != "?":
                dts.labels[source].append((role, lang, text))
            dts.arcs.append(
                Arc("label", elr, arcrole, source, f"label:{role}:{lang}", attrs)
            )
        elif res.tag == LINK_REFERENCE or arcrole == CONCEPT_REFERENCE_ARCROLE:
            parts = {"role": role}
            for part in res:
                _, local = split_clark(part.tag)
                parts[local] = " ".join((part.text or "").split())
            if source != "?":
                dts.references[source].append(parts)
            dts.arcs.append(
                Arc("reference", elr, arcrole, source, f"reference:{role}", attrs)
            )
        else:
            dts.arcs.append(
                Arc(linkbase, elr, arcrole, source, f"resource:{res.tag}", attrs)
            )


# ── packages ──────────────────────────────────────────────────────────────


def unpack_package(path: Path, workdir: Path) -> Path:
    """Extract a .zip / .xbri into workdir and return the extraction root."""
    target = workdir / path.stem
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path) as zf:
        for member in zf.infolist():
            # Refuse members that would escape the extraction root.
            dest = (target / member.filename).resolve()
            if not str(dest).startswith(str(target.resolve())):
                raise ValueError(
                    f"{path}: member escapes archive root: {member.filename}"
                )
        zf.extractall(target)
    return target


def package_catalogs(extracted: Path) -> list[Path]:
    return sorted(extracted.rglob("META-INF/catalog.xml"))


def package_starts(extracted: Path) -> list[str]:
    """Entry points of a taxonomy package, or the reports of a report package.

    Taxonomy Packages 1.0 section 3.2.2: `tp:entryPointDocument/@href`,
    resolved against the manifest. Report Packages 1.0: the documents under
    `reports/`. A package may be both, and then both sets are starts.
    """
    starts: list[str] = []
    for manifest in sorted(extracted.rglob("META-INF/taxonomyPackage.xml")):
        tree = etree.parse(str(manifest), secure_parser())
        base = manifest.resolve().as_uri()
        for ep in tree.getroot().iter(TP_ENTRY_POINT_DOCUMENT):
            href = ep.get("href")
            if href:
                starts.append(join(base, href))
    for reports in sorted(extracted.rglob("reports")):
        if reports.is_dir():
            for f in sorted(reports.rglob("*")):
                if f.suffix.lower() in (".xhtml", ".html", ".xml", ".xbrl"):
                    starts.append(f.resolve().as_uri())
    return starts


# ── profile ───────────────────────────────────────────────────────────────


def presentation_networks(dts: DTS) -> list[dict[str, Any]]:
    """Per ELR: nodes, arcs, roots and the depth of the deepest path.

    Prohibited arcs are skipped; priority-based override of a non-prohibited
    arc by another is not resolved (that is a validator's job), so a network
    that relies on it may read one level deeper here than in Arelle.
    """
    by_elr: dict[str, list[Arc]] = defaultdict(list)
    for arc in dts.arcs:
        if arc.linkbase == "presentation" and arc.attrs.get("use") != "prohibited":
            by_elr[arc.elr].append(arc)
    out: list[dict[str, Any]] = []
    for elr, arcs in sorted(by_elr.items()):
        children: dict[str, list[str]] = defaultdict(list)
        nodes: set[str] = set()
        for arc in arcs:
            children[arc.source].append(arc.target)
            nodes.update((arc.source, arc.target))
        targets = {arc.target for arc in arcs}
        roots = sorted(n for n in nodes if n not in targets)
        depth = 0
        stack = [(r, 1, frozenset({r})) for r in roots]
        while stack:
            node, d, seen = stack.pop()
            depth = max(depth, d)
            for c in children.get(node, []):
                if c not in seen:
                    stack.append((c, d + 1, seen | {c}))
        out.append(
            {
                "elr": elr,
                "definition": dts.role_types.get(elr, {}).get("definition", ""),
                "nodes": len(nodes),
                "arcs": len(arcs),
                "roots": len(roots),
                "depth": depth,
            }
        )
    return out


def profile(dts: DTS) -> dict[str, Any]:
    docs = list(dts.documents.values())
    doc_kinds = Counter(d.kind for d in docs)
    concepts = list(dts.concepts.values())
    items = [c for c in concepts if c.root == "item"]
    pres = presentation_networks(dts)
    calc_arcs = [a for a in dts.arcs if a.linkbase == "calculation"]
    def_arcs = [a for a in dts.arcs if a.linkbase == "definition"]
    label_roles: Counter[str] = Counter()
    label_langs: Counter[str] = Counter()
    for rows in dts.labels.values():
        for role, lang, _ in rows:
            label_roles[role] += 1
            label_langs[lang] += 1
    ref_parts: Counter[str] = Counter()
    for rows in dts.references.values():
        for parts in rows:
            for k in parts:
                if k != "role":
                    ref_parts[k] += 1
    hypercubes = [c for c in concepts if c.root == "hypercubeItem"]
    dimensions = [c for c in concepts if c.root == "dimensionItem"]
    xdt_arcroles = Counter(
        a.arcrole for a in def_arcs if a.arcrole.startswith(XDT_ARCROLE_PREFIX)
    )
    other_def_arcroles = Counter(
        a.arcrole for a in def_arcs if not a.arcrole.startswith(XDT_ARCROLE_PREFIX)
    )
    domain_members = {
        a.target for a in def_arcs if a.arcrole == XDT_ARCROLE_PREFIX + "domain-member"
    }
    primary_items = {
        a.source
        for a in def_arcs
        if a.arcrole in (XDT_ARCROLE_PREFIX + "all", XDT_ARCROLE_PREFIX + "notAll")
    }
    without_standard_label = sum(
        1
        for c in items
        if not any(
            role == STANDARD_LABEL_ROLE for role, _, _ in dts.labels.get(c.qname, [])
        )
    )
    depths = sorted(n["depth"] for n in pres)
    return {
        "starts": dts.starts,
        "documents": {
            "total": len(dts.documents),
            "by_kind": dict(doc_kinds),
            "by_host": dict(Counter(host_of(u) for u in dts.documents)),
            "by_source": dict(Counter(d.source for d in docs)),
            "boundary_not_followed": sorted(dts.boundary),
            "unresolved": dict(sorted(dts.unresolved.items())),
        },
        "discovery_pointers": dict(Counter(kind for _, kind, _ in dts.discovery)),
        "concepts": {
            "total": len(concepts),
            "by_substitution_root": dict(Counter(c.root or "?" for c in concepts)),
            "abstract": sum(1 for c in concepts if c.abstract),
            "concrete_items": sum(1 for c in items if not c.abstract),
            "by_period_type": dict(Counter(c.period_type or "(none)" for c in items)),
            "by_balance": dict(Counter(c.balance or "(none)" for c in items)),
            "by_type": dict(Counter(c.type_bucket for c in items).most_common()),
            "by_namespace": dict(
                Counter(split_clark(c.qname)[0] for c in concepts).most_common(12)
            ),
            "nillable_false": sum(1 for c in items if not c.nillable),
        },
        "role_types": {
            "total": len(dts.role_types),
            "by_usedOn": dict(
                Counter(u for rt in dts.role_types.values() for u in rt["usedOn"])
            ),
        },
        "arcrole_types": {
            "total": len(dts.arcrole_types),
            "uris": sorted(dts.arcrole_types),
        },
        "presentation": {
            "networks": len(pres),
            "arcs": sum(n["arcs"] for n in pres),
            "prohibited_arcs": sum(
                1
                for a in dts.arcs
                if a.linkbase == "presentation" and a.attrs.get("use") == "prohibited"
            ),
            "depth_max": depths[-1] if depths else 0,
            "depth_median": depths[len(depths) // 2] if depths else 0,
            "preferred_labels": dict(
                Counter(
                    a.attrs["preferredLabel"]
                    for a in dts.arcs
                    if a.linkbase == "presentation" and "preferredLabel" in a.attrs
                ).most_common()
            ),
        },
        "calculation": {
            "networks": len({a.elr for a in calc_arcs}),
            "arcs": len(calc_arcs),
            "arcroles": dict(Counter(a.arcrole for a in calc_arcs)),
            "weights": dict(Counter(a.attrs.get("weight", "?") for a in calc_arcs)),
        },
        "definition": {
            "networks": len({a.elr for a in def_arcs}),
            "arcs": len(def_arcs),
            "xdt_arcroles": dict(xdt_arcroles.most_common()),
            "other_arcroles": dict(other_def_arcroles.most_common()),
            "hypercubes": len(hypercubes),
            "dimensions_explicit": sum(1 for d in dimensions if not d.typed_domain_ref),
            "dimensions_typed": sum(1 for d in dimensions if d.typed_domain_ref),
            "domain_members_distinct": len(domain_members),
            "primary_items_with_hypercube": len(primary_items),
        },
        "labels": {
            "resources": sum(label_roles.values()),
            "concepts_with_labels": len(dts.labels),
            "items_without_standard_label": without_standard_label,
            "by_role": dict(label_roles.most_common()),
            "by_language": dict(label_langs.most_common()),
        },
        "references": {
            "resources": sum(len(v) for v in dts.references.values()),
            "concepts_with_references": len(dts.references),
            "parts": dict(ref_parts.most_common()),
        },
        "generic_links": dict(dts.generic_links.most_common()),
        "resources_by_kind": dict(dts.resources_by_kind.most_common()),
        "unresolved_locators": dts.unresolved_locators,
        "unresolved_locators_by_kind": dict(dts.unresolved_locator_kinds.most_common()),
        "unresolved_locators_by_document": dict(
            dts.unresolved_locator_docs.most_common(10)
        ),
        "presentation_networks": pres,
    }


def concept_view(dts: DTS, query: str) -> dict[str, Any] | None:
    qname = find_concept(dts, query)
    if qname is None:
        return None
    c = dts.concepts[qname]
    ns, local = split_clark(qname)
    edges: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for a in dts.arcs:
        if a.linkbase in ("presentation", "calculation", "definition") and qname in (
            a.source,
            a.target,
        ):
            edges[a.linkbase].append(
                {
                    "elr": a.elr,
                    "arcrole": a.arcrole,
                    "direction": "child" if a.source == qname else "parent",
                    "other": display(dts, a.target if a.source == qname else a.source),
                    **a.attrs,
                }
            )
    return {
        "qname": display(dts, qname),
        "namespace": ns,
        "name": local,
        "declared_in": c.doc,
        "id": c.id,
        "type": display(dts, c.type) if c.type else None,
        "substitution_group": display(dts, c.substitution_group)
        if c.substitution_group
        else None,
        "root": c.root,
        "abstract": c.abstract,
        "nillable": c.nillable,
        "period_type": c.period_type,
        "balance": c.balance,
        "typed_domain_ref": c.typed_domain_ref,
        "labels": [
            {"role": r, "lang": lang, "text": t}
            for r, lang, t in sorted(dts.labels.get(qname, []))
        ],
        "references": dts.references.get(qname, []),
        "presentation": sorted(
            edges["presentation"], key=lambda e: (e["elr"], e["direction"])
        ),
        "calculation": sorted(
            edges["calculation"], key=lambda e: (e["elr"], e["direction"])
        ),
        "definition": sorted(
            edges["definition"], key=lambda e: (e["elr"], e["arcrole"])
        ),
    }


def find_concept(dts: DTS, query: str) -> str | None:
    if query in dts.concepts:
        return query
    if query.startswith("{"):
        return None
    prefix, sep, local = query.partition(":")
    if sep:
        for ns, p in dts.prefixes.items():
            if p == prefix and f"{{{ns}}}{local}" in dts.concepts:
                return f"{{{ns}}}{local}"
        # Fall back to matching the namespace by its last path segment.
        hits = [
            q
            for q in dts.concepts
            if split_clark(q)[1] == local
            and split_clark(q)[0].rstrip("/").split("/")[-1] == prefix
        ]
        return hits[0] if len(hits) == 1 else None
    hits = [q for q in dts.concepts if split_clark(q)[1] == query]
    return hits[0] if len(hits) == 1 else None


def display(dts: DTS, qname: str) -> str:
    ns, local = split_clark(qname)
    prefix = dts.prefixes.get(ns)
    return f"{prefix}:{local}" if prefix else qname


# ── rendering ─────────────────────────────────────────────────────────────


def table(rows: dict[str, Any], left: str = "key", right: str = "count") -> list[str]:
    out = [f"| {left} | {right} |", "|---|---|"]
    for k, v in rows.items():
        out.append(f"| {k or '(empty)'} | {v} |")
    return out


def render_markdown(p: dict[str, Any]) -> str:
    d, c = p["documents"], p["concepts"]
    lines = ["# DTS profile", "", "Start: " + ", ".join(p["starts"]), ""]
    lines += [
        "## Documents",
        "",
        f"Total {d['total']}; by kind {d['by_kind']}; by source {d['by_source']}.",
        "",
        *table(d["by_host"], "host", "documents"),
        "",
        f"Boundary (infrastructure, not followed): {len(d['boundary_not_followed'])}",
        f"Unresolved: {len(d['unresolved'])}",
    ]
    for uri, reason in d["unresolved"].items():
        lines.append(f"- UNRESOLVED {uri}: {reason}")
    lines += [
        "",
        "## Discovery pointers",
        "",
        *table(p["discovery_pointers"], "pointer", "edges"),
    ]
    lines += [
        "",
        "## Concepts",
        "",
        f"Total {c['total']} (abstract {c['abstract']}, "
        f"concrete items {c['concrete_items']}, "
        f"nillable=false items {c['nillable_false']}).",
        "",
        *table(c["by_substitution_root"], "substitution root", "concepts"),
        "",
        *table(c["by_period_type"], "periodType (items)", "concepts"),
        "",
        *table(c["by_balance"], "balance (items)", "concepts"),
        "",
        *table(c["by_type"], "type bucket (items)", "concepts"),
        "",
        *table(c["by_namespace"], "namespace", "concepts"),
    ]
    r = p["role_types"]
    lines += [
        "",
        "## Role and arcrole types",
        "",
        f"roleType {r['total']}; usedOn {r['by_usedOn']}; "
        f"arcroleType {p['arcrole_types']['total']}.",
    ]
    pr = p["presentation"]
    lines += [
        "",
        "## Presentation",
        "",
        f"Networks {pr['networks']}; arcs {pr['arcs']} "
        f"(+{pr['prohibited_arcs']} prohibited); "
        f"depth max {pr['depth_max']}, median {pr['depth_median']}.",
        "",
        *table(pr["preferred_labels"], "preferredLabel", "arcs"),
    ]
    ca = p["calculation"]
    lines += [
        "",
        "## Calculation",
        "",
        f"Networks {ca['networks']}; arcs {ca['arcs']}; arcroles {ca['arcroles']}; "
        f"weights {ca['weights']}.",
    ]
    de = p["definition"]
    lines += [
        "",
        "## Definition and dimensions",
        "",
        f"Networks {de['networks']}; arcs {de['arcs']}; hypercubes {de['hypercubes']}; "
        f"dimensions explicit {de['dimensions_explicit']}, "
        f"typed {de['dimensions_typed']}; "
        f"distinct domain members {de['domain_members_distinct']}; "
        f"primary items with a hypercube {de['primary_items_with_hypercube']}.",
        "",
        *table(de["xdt_arcroles"], "XDT arcrole", "arcs"),
        "",
        *table(de["other_arcroles"], "other definition arcrole", "arcs"),
    ]
    la = p["labels"]
    lines += [
        "",
        "## Labels",
        "",
        f"Resources {la['resources']} on {la['concepts_with_labels']} concepts; "
        f"items without a standard label {la['items_without_standard_label']}.",
        "",
        *table(la["by_role"], "label role", "labels"),
        "",
        *table(la["by_language"], "language", "labels"),
    ]
    re_ = p["references"]
    lines += [
        "",
        "## References",
        "",
        f"Resources {re_['resources']} on {re_['concepts_with_references']} concepts.",
        "",
        *table(re_["parts"], "reference part", "occurrences"),
    ]
    lines += [
        "",
        "## Generic links and other resources",
        "",
        f"Generic extended links {p['generic_links']}",
        f"Resources by kind {p['resources_by_kind']}",
        f"Unresolved locators {p['unresolved_locators']}: "
        f"{p['unresolved_locators_by_kind']}",
        "",
        *table(p["unresolved_locators_by_document"], "document", "unresolved locators"),
        "",
        "## Presentation networks (deepest first)",
        "",
        "| depth | nodes | arcs | roots | ELR | definition |",
        "|---|---|---|---|---|---|",
    ]
    for n in sorted(p["presentation_networks"], key=lambda n: (-n["depth"], n["elr"]))[
        :40
    ]:
        lines.append(
            f"| {n['depth']} | {n['nodes']} | {n['arcs']} | {n['roots']} | "
            f"{n['elr']} | {n['definition']} |"
        )
    if len(p["presentation_networks"]) > 40:
        lines.append(f"| ... | | | | {len(p['presentation_networks']) - 40} more | |")
    return "\n".join(lines) + "\n"


def render_concept(v: dict[str, Any]) -> str:
    lines = [
        f"# {v['qname']}",
        "",
        f"- namespace: {v['namespace']}",
        f"- declared in: {v['declared_in']} (id {v['id']})",
        f"- type: {v['type']}; substitutionGroup: {v['substitution_group']} "
        f"(root {v['root']})",
        f"- abstract: {v['abstract']}; nillable: {v['nillable']}; "
        f"periodType: {v['period_type']}; balance: {v['balance']}",
    ]
    if v["typed_domain_ref"]:
        lines.append(f"- typedDomainRef: {v['typed_domain_ref']}")
    lines += ["", "## Labels", "", "| role | lang | text |", "|---|---|---|"]
    for lab in v["labels"]:
        lines.append(f"| {lab['role']} | {lab['lang']} | {lab['text']} |")
    lines += ["", "## References", ""]
    for ref in v["references"]:
        lines.append("- " + "; ".join(f"{k}={val}" for k, val in ref.items()))
    for kind in ("presentation", "calculation", "definition"):
        lines += ["", f"## {kind.capitalize()} edges", ""]
        for e in v[kind]:
            extra = {
                k: val
                for k, val in e.items()
                if k not in ("elr", "arcrole", "direction", "other")
            }
            lines.append(
                f"- [{e['direction']}] {e['other']} in {e['elr']} "
                f"({e['arcrole']}) {extra}"
            )
    return "\n".join(lines) + "\n"


# ── entry point ───────────────────────────────────────────────────────────


def build(
    starts: list[str],
    packages: list[str],
    cache_dir: Path | None,
    offline: bool,
    follow_infrastructure: bool,
    max_documents: int,
) -> DTS:
    workdir = Path(tempfile.mkdtemp(prefix="dts-profile-"))
    try:
        catalog = Catalog()
        resolved_starts: list[str] = []
        for pkg in packages:
            extracted = unpack_package(Path(pkg).expanduser(), workdir)
            for cat in package_catalogs(extracted):
                catalog.load(cat)
        for start in starts:
            path = Path(start).expanduser()
            if path.suffix.lower() in (".zip", ".xbri") and path.is_file():
                extracted = unpack_package(path, workdir)
                for cat in package_catalogs(extracted):
                    catalog.load(cat)
                resolved_starts.extend(package_starts(extracted))
            else:
                resolved_starts.append(to_uri(start))
        walker = Walker(
            Fetcher(cache_dir, offline), catalog, follow_infrastructure, max_documents
        )
        dts = walker.discover(resolved_starts)
        dts.starts = [*starts]
        return dts
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("starts", nargs="+", metavar="START")
    parser.add_argument("--package", action="append", default=[], metavar="PKG")
    parser.add_argument(
        "--cache-dir", default=str(Path.home() / ".cache" / "ixbrl-skill" / "dts")
    )
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--follow-infrastructure", action="store_true")
    parser.add_argument("--max-documents", type=int, default=DEFAULT_MAX_DOCUMENTS)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--concept", metavar="QNAME")
    args = parser.parse_args(argv)

    for start in args.starts:
        if not is_url(start) and not Path(start).expanduser().exists():
            sys.stderr.write(f"no such start: {start}\n")
            return 2
    cache_dir = None if args.no_cache else Path(args.cache_dir).expanduser()
    try:
        dts = build(
            args.starts,
            args.package,
            cache_dir,
            args.offline,
            args.follow_infrastructure,
            args.max_documents,
        )
    except (zipfile.BadZipFile, ValueError, etree.XMLSyntaxError) as exc:
        sys.stderr.write(f"cannot read start: {exc}\n")
        return 2

    if args.concept:
        view = concept_view(dts, args.concept)
        if view is None:
            sys.stderr.write(
                f"concept not found in this DTS: {args.concept} "
                f"(known prefixes: {sorted(set(dts.prefixes.values()))})\n"
            )
            return 1
        sys.stdout.write(
            json.dumps(view, indent=2) if args.json else render_concept(view)
        )
    else:
        p = profile(dts)
        sys.stdout.write(
            json.dumps(p, indent=2) + "\n" if args.json else render_markdown(p)
        )
    return 1 if dts.unresolved or dts.unresolved_locators else 0


if __name__ == "__main__":
    raise SystemExit(main())
