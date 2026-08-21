#!/usr/bin/env python3
"""Tests for scripts/dts_profile.py.

Hermetic: every test walks either the bundled scaffold under assets/ (a real
five-document DTS with XDT, nine label roles and two languages) or a fixture
written into a temporary directory. Nothing is fetched; the XBRL and W3C
infrastructure schemas the scaffold imports sit on the boundary the script
records but does not follow, and `--offline` is asserted to fail closed with
a reason rather than reach for the network.

The counts asserted against the scaffold were cross-checked against Arelle
2.41.7 on three production taxonomies (IFRS 2025, ESEF 2024, NT/KvK 2025)
when the script was written; that comparison is recorded in the pull request
that added it, not re-run here.

Uses stdlib unittest, matching tests/test_check_facts.py.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""

from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
import zipfile
from collections import Counter
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import dts_profile

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
SCHEMA = ASSETS / "extension-schema.xsd"
EXT_NS = "http://example.com/extension"
LABEL = "http://www.xbrl.org/2003/role/label"
NEGATED = "http://www.xbrl.org/2009/role/negatedLabel"
XDT = "http://xbrl.org/int/dim/arcrole/"


def walk(*starts: str, packages: list[str] | None = None, **kw) -> dts_profile.DTS:
    return dts_profile.build(
        list(starts),
        packages or [],
        cache_dir=None,
        offline=kw.get("offline", True),
        follow_infrastructure=kw.get("follow_infrastructure", False),
        max_documents=kw.get("max_documents", 5000),
    )


def run_main(*argv: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = dts_profile.main(list(argv))
    return code, out.getvalue(), err.getvalue()


class ScaffoldDiscoveryTestCase(unittest.TestCase):
    """The discovery closure of the bundled scaffold, by XBRL 2.1 section 3.2."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.dts = walk(str(SCHEMA))
        cls.profile = dts_profile.profile(cls.dts)

    def test_closure_is_schema_plus_four_linkbases(self):
        """The schema's appinfo linkbaseRefs pull in exactly the four linkbases.

        Asserts the document kinds, not just a count: a walk that followed a
        locator into a linkbase it should have reached through linkbaseRef
        would produce the same number for a different reason.
        """
        kinds = sorted(d.kind for d in self.dts.documents.values())
        self.assertEqual(kinds, ["linkbase"] * 4 + ["schema"])
        self.assertEqual(self.dts.unresolved, {})

    def test_infrastructure_imports_are_boundary_not_unresolved(self):
        """xbrl.org / w3.org imports are recorded as a boundary, never as errors."""
        hosts = {dts_profile.host_of(u) for u in self.dts.boundary}
        self.assertTrue(hosts <= dts_profile.INFRASTRUCTURE_HOSTS, hosts)
        self.assertGreaterEqual(len(self.dts.boundary), 5)
        self.assertNotIn("xbrl.org", " ".join(self.dts.unresolved))

    def test_discovery_pointer_kinds(self):
        pointers = self.profile["discovery_pointers"]
        self.assertEqual(pointers["start"], 1)
        self.assertEqual(pointers["linkbaseRef"], 4)
        self.assertGreaterEqual(pointers["import"], 4)

    def test_concepts_by_substitution_root(self):
        roots = self.profile["concepts"]["by_substitution_root"]
        self.assertEqual(roots["hypercubeItem"], 1)
        self.assertEqual(roots["dimensionItem"], 2)
        self.assertGreater(roots["item"], 15)
        self.assertEqual(self.profile["concepts"]["by_namespace"], {EXT_NS: 25})

    def test_typed_and_explicit_dimensions_are_told_apart(self):
        d = self.profile["definition"]
        self.assertEqual((d["dimensions_explicit"], d["dimensions_typed"]), (1, 1))
        self.assertEqual(d["hypercubes"], 1)
        self.assertEqual(d["xdt_arcroles"][XDT + "all"], 1)
        self.assertEqual(d["xdt_arcroles"][XDT + "hypercube-dimension"], 2)
        self.assertEqual(d["xdt_arcroles"][XDT + "dimension-default"], 1)

    def test_presentation_depth_skips_prohibited_arcs(self):
        pr = self.profile["presentation"]
        self.assertEqual(pr["networks"], 1)
        self.assertEqual(pr["prohibited_arcs"], 1)
        self.assertEqual(pr["depth_max"], 3)
        self.assertIn(NEGATED, pr["preferred_labels"])

    def test_calculation_weights(self):
        self.assertEqual(self.profile["calculation"]["weights"], {"1": 2, "-1": 2})

    def test_labels_by_role_and_language(self):
        la = self.profile["labels"]
        self.assertEqual(la["by_language"], {"en": 12, "nl": 1})
        self.assertEqual(la["by_role"][LABEL], 4)
        self.assertEqual(la["by_role"][NEGATED], 1)
        self.assertEqual(la["resources"], 13)

    def test_role_types_and_used_on(self):
        rt = self.profile["role_types"]
        self.assertEqual(rt["total"], 4)
        self.assertEqual(rt["by_usedOn"]["link:definitionLink"], 4)

    def test_markdown_rendering_lists_every_section(self):
        text = dts_profile.render_markdown(self.profile)
        for heading in (
            "## Documents",
            "## Concepts",
            "## Presentation",
            "## Calculation",
            "## Definition and dimensions",
            "## Labels",
            "## References",
        ):
            self.assertIn(heading, text)
        self.assertIn("Unresolved: 0", text)


class ConceptViewTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dts = walk(str(SCHEMA))

    def test_prefix_resolves_through_the_schema_declared_prefix(self):
        view = dts_profile.concept_view(self.dts, "ext:Assets")
        self.assertIsNotNone(view)
        assert view is not None
        self.assertEqual(view["name"], "Assets")
        self.assertEqual(view["period_type"], "instant")
        self.assertEqual(view["balance"], "debit")
        self.assertEqual(view["root"], "item")

    def test_labels_carry_role_and_language(self):
        view = dts_profile.concept_view(self.dts, "ext:ExampleMonetaryConceptInstant")
        assert view is not None
        pairs = {(lab["role"], lab["lang"]) for lab in view["labels"]}
        self.assertIn((LABEL, "en"), pairs)
        self.assertIn((LABEL, "nl"), pairs)
        self.assertIn((NEGATED, "en"), pairs)

    def test_calculation_edges_carry_weight_and_direction(self):
        view = dts_profile.concept_view(self.dts, "ext:OperatingProfit")
        assert view is not None
        self.assertEqual(len(view["calculation"]), 4, "OperatingProfit sums four")
        self.assertEqual(
            sorted(e["weight"] for e in view["calculation"]), ["-1", "-1", "1", "1"]
        )
        self.assertTrue(all(e["direction"] == "child" for e in view["calculation"]))
        child = dts_profile.concept_view(self.dts, "ext:CostOfSales")
        assert child is not None
        self.assertEqual(child["calculation"][0]["direction"], "parent")
        self.assertEqual(child["calculation"][0]["other"], "ext:OperatingProfit")

    def test_unknown_concept_is_none_and_main_exits_one(self):
        self.assertIsNone(dts_profile.concept_view(self.dts, "ext:NoSuchThing"))
        code, _, err = run_main(
            str(SCHEMA), "--offline", "--no-cache", "--concept", "ext:Nope"
        )
        self.assertEqual(code, 1)
        self.assertIn("concept not found", err)

    def test_bare_local_name_resolves_when_unique(self):
        self.assertEqual(
            dts_profile.find_concept(self.dts, "Assets"), f"{{{EXT_NS}}}Assets"
        )


class CatalogAndPackageTestCase(unittest.TestCase):
    """Taxonomy-package resolution: catalog rewrites, entry points, identity."""

    def make_package(self, tmp: Path, catalog_prefix: str) -> Path:
        """A package whose catalog maps catalog_prefix/ onto a copy of assets/."""
        root = tmp / "pkg" / "example-2024"
        (root / "META-INF").mkdir(parents=True)
        files = root / "files"
        files.mkdir()
        for name in (
            "extension-schema.xsd",
            "label-linkbase.xml",
            "presentation-linkbase.xml",
            "calculation-linkbase.xml",
            "definition-linkbase.xml",
        ):
            (files / name).write_bytes((ASSETS / name).read_bytes())
        (root / "META-INF" / "catalog.xml").write_text(
            '<?xml version="1.0"?>'
            '<catalog xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog">'
            f'<rewriteURI uriStartString="{catalog_prefix}" rewritePrefix="../files/"/>'
            f'<rewriteURI uriStartString="{catalog_prefix}deeper/" '
            'rewritePrefix="../nowhere/"/>'
            "</catalog>"
        )
        (root / "META-INF" / "taxonomyPackage.xml").write_text(
            '<?xml version="1.0"?>'
            '<tp:taxonomyPackage xmlns:tp="http://xbrl.org/2016/taxonomy-package">'
            "<tp:identifier>http://example.com/pkg</tp:identifier>"
            "<tp:entryPoints><tp:entryPoint>"
            f'<tp:entryPointDocument href="{catalog_prefix}extension-schema.xsd"/>'
            "</tp:entryPoint></tp:entryPoints></tp:taxonomyPackage>"
        )
        zip_path = tmp / "example.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            for f in sorted(root.rglob("*")):
                if f.is_file():
                    zf.write(f, f.relative_to(tmp / "pkg"))
        return zip_path

    def test_remote_start_resolves_offline_through_the_catalog(self):
        """A canonical https URI is read from the package, keyed by its own URI.

        Keying by the canonical URI is what the test is really about: the
        host column must say example.com, not (local), or a profile could not
        tell a taxonomy read from a package apart from a local file.
        """
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            pkg = self.make_package(tmp, "https://example.com/taxonomy/2024/")
            dts = walk(
                "https://example.com/taxonomy/2024/extension-schema.xsd",
                packages=[str(pkg)],
            )
            self.assertEqual(dts.unresolved, {})
            self.assertEqual(len(dts.documents), 5)
            hosts = {dts_profile.host_of(u) for u in dts.documents}
            self.assertEqual(hosts, {"example.com"})
            self.assertTrue(
                all(d.source.startswith("package") for d in dts.documents.values())
            )

    def test_package_as_start_uses_its_entry_points(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            pkg = self.make_package(tmp, "https://example.com/taxonomy/2024/")
            dts = walk(str(pkg))
            self.assertEqual(dts.unresolved, {})
            self.assertEqual(len(dts.concepts), 25)

    def test_longest_matching_prefix_wins(self):
        """XML Catalogs 1.1 section 7.2.2: the longest uriStartString applies."""
        cat = dts_profile.Catalog()
        cat.entries = [
            ("https://e.com/", "file:///short/"),
            ("https://e.com/deep/", "file:///long/"),
        ]
        cat.entries.sort(key=lambda item: len(item[0]), reverse=True)
        self.assertEqual(cat.rewrite("https://e.com/deep/x.xsd"), "file:///long/x.xsd")
        self.assertEqual(cat.rewrite("https://e.com/y.xsd"), "file:///short/y.xsd")
        self.assertEqual(cat.rewrite("https://other/z.xsd"), "https://other/z.xsd")

    def test_zip_member_escaping_the_root_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            bad = Path(d) / "bad.zip"
            with zipfile.ZipFile(bad, "w") as zf:
                zf.writestr("../../escape.xsd", "<x/>")
            with self.assertRaises(ValueError):
                dts_profile.unpack_package(bad, Path(d) / "out")

    def test_zip_member_escaping_into_a_sibling_directory_is_refused(self):
        """A sibling path shares the root's string prefix and is outside it.

        `out/bad/../../bad-evil/x` resolves to `<workdir>/bad-evil/x`, whose
        string starts with `<workdir>/bad`; a prefix test accepted it.
        """
        with tempfile.TemporaryDirectory() as d:
            bad = Path(d) / "bad.zip"
            with zipfile.ZipFile(bad, "w") as zf:
                zf.writestr("../../bad-evil/escape.xsd", "<x/>")
            with self.assertRaises(ValueError):
                dts_profile.unpack_package(bad, Path(d) / "out")
            self.assertFalse((Path(d) / "bad-evil").exists())
            self.assertFalse((Path(d) / "out" / "bad-evil").exists())

    def test_package_with_neither_entry_points_nor_reports_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            empty = Path(d) / "empty.zip"
            with zipfile.ZipFile(empty, "w") as zf:
                zf.writestr("empty/META-INF/taxonomyPackage.xml", "<x/>")
            code, _, err = run_main(str(empty), "--offline", "--no-cache")
            self.assertEqual(code, 2)
            self.assertIn("nothing to walk", err)

    def test_prohibited_calculation_arcs_are_not_counted(self):
        schema = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" '
            'xmlns:xbrli="http://www.xbrl.org/2003/instance" '
            'xmlns:link="http://www.xbrl.org/2003/linkbase" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'targetNamespace="http://t.example/c">'
            "<xs:annotation><xs:appinfo><link:linkbase>"
            '<link:calculationLink xlink:type="extended" '
            'xlink:role="http://www.xbrl.org/2003/role/link">'
            '<link:loc xlink:type="locator" xlink:href="#c_A" xlink:label="a"/>'
            '<link:loc xlink:type="locator" xlink:href="#c_B" xlink:label="b"/>'
            '<link:calculationArc xlink:type="arc" xlink:from="a" xlink:to="b" '
            'xlink:arcrole="http://www.xbrl.org/2003/arcrole/summation-item" '
            'weight="1" use="prohibited" priority="1"/>'
            "</link:calculationLink></link:linkbase></xs:appinfo></xs:annotation>"
            '<xs:element name="A" id="c_A" substitutionGroup="xbrli:item" '
            'type="xbrli:monetaryItemType" xbrli:periodType="instant"/>'
            '<xs:element name="B" id="c_B" substitutionGroup="xbrli:item" '
            'type="xbrli:monetaryItemType" xbrli:periodType="instant"/>'
            "</xs:schema>"
        )
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "c.xsd"
            path.write_text(schema)
            p = dts_profile.profile(walk(str(path)))
            self.assertEqual(p["calculation"]["arcs"], 0)
            self.assertEqual(p["calculation"]["prohibited_arcs"], 1)


class FailureModesTestCase(unittest.TestCase):
    def test_offline_remote_start_fails_closed_with_a_reason(self):
        dts = walk("https://example.invalid/entry.xsd")
        self.assertEqual(
            dts.unresolved,
            {"https://example.invalid/entry.xsd": "offline and not in cache"},
        )
        self.assertEqual(dts.documents, {})

    def test_inline_xbrl_start_reports_its_dangling_schemaref(self):
        """The scaffold's schemaRef names a file that does not ship: say so.

        This is the real artifact the repository bundles, not a fixture shaped
        like one, and it exercises the path a preparer hits first: an Inline
        XBRL document whose `ix:references` points at an extension schema that
        is not where the href says.
        """
        skeleton = ASSETS / "ixbrl-skeleton.xhtml"
        dts = walk(str(skeleton))
        self.assertEqual(len(dts.documents), 1)
        self.assertEqual(dts.documents[skeleton.resolve().as_uri()].kind, "inline")
        self.assertEqual(len(dts.unresolved), 1)
        ((uri, reason),) = dts.unresolved.items()
        self.assertTrue(uri.endswith("example-extension.xsd"))
        self.assertIn("no such file", reason)
        code, out, _ = run_main(
            str(ASSETS / "ixbrl-skeleton.xhtml"), "--offline", "--no-cache"
        )
        self.assertEqual(code, 1)
        self.assertIn("UNRESOLVED", out)

    def test_malformed_document_is_reported_not_raised(self):
        with tempfile.TemporaryDirectory() as d:
            bad = Path(d) / "bad.xsd"
            bad.write_text(
                "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><oops"
            )
            dts = walk(str(bad))
            (reason,) = dts.unresolved.values()
            self.assertIn("not well-formed", reason)

    def test_missing_start_is_a_usage_error(self):
        code, _, err = run_main("/no/such/file.xsd", "--offline", "--no-cache")
        self.assertEqual(code, 2)
        self.assertIn("no such start", err)

    def test_max_documents_bounds_the_walk_visibly(self):
        dts = walk(str(SCHEMA), max_documents=1)
        self.assertEqual(len(dts.documents), 1)
        self.assertEqual(len(dts.unresolved), 4)
        self.assertTrue(all("--max-documents" in r for r in dts.unresolved.values()))

    def test_substitution_group_chain_through_an_intermediate_group(self):
        """An element whose chain reaches xbrli:item through a taxonomy-defined
        group is a concept; one whose chain goes nowhere is not, and the
        difference is decided by walking the chain, never by the literal
        attribute value.
        """
        schema = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" '
            'xmlns:xbrli="http://www.xbrl.org/2003/instance" '
            'xmlns:t="http://t.example/t" targetNamespace="http://t.example/t">'
            '<xs:element name="presentationItem" abstract="true" '
            'substitutionGroup="xbrli:item" type="xbrli:stringItemType" '
            'xbrli:periodType="duration"/>'
            '<xs:element name="Revenue" substitutionGroup="t:presentationItem" '
            'type="xbrli:monetaryItemType" xbrli:periodType="duration" '
            'xbrli:balance="credit"/>'
            '<xs:element name="Helper" substitutionGroup="t:nothing" '
            'type="xs:string"/>'
            '<xs:element name="Plain" type="xs:string"/>'
            "</xs:schema>"
        )
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "t.xsd"
            path.write_text(schema)
            dts = walk(str(path))
            names = sorted(dts_profile.split_clark(q)[1] for q in dts.concepts)
            self.assertEqual(names, ["Revenue", "presentationItem"])
            self.assertEqual(dts.concepts["{http://t.example/t}Revenue"].root, "item")

    def test_embedded_linkbase_locators_discover_other_schemas(self):
        """A locator inside a schema-embedded linkbase is a discovery pointer.

        XBRL 2.1 section 3.2 counts linkbases at
        //xsd:schema/xsd:annotation/xsd:appinfo/* as discovered, and every
        locator in a discovered linkbase discovers the schema it points
        into. The US-GAAP 2025 core schema reaches the SEC state/province
        schema (65 concepts) only through such an embedded locator; a walk
        that read embedded linkbases but did not follow their locators
        missed them, and Arelle did not.
        """
        other = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" '
            'xmlns:xbrli="http://www.xbrl.org/2003/instance" '
            'targetNamespace="http://t.example/other">'
            '<xs:element name="TX" id="other_TX" substitutionGroup="xbrli:item" '
            'type="xbrli:stringItemType" xbrli:periodType="duration"/>'
            "</xs:schema>"
        )
        main = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" '
            'xmlns:xbrli="http://www.xbrl.org/2003/instance" '
            'xmlns:link="http://www.xbrl.org/2003/linkbase" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'targetNamespace="http://t.example/main">'
            "<xs:annotation><xs:appinfo><link:linkbase>"
            '<link:definitionLink xlink:type="extended" '
            'xlink:role="http://www.xbrl.org/2003/role/link">'
            '<link:loc xlink:type="locator" xlink:href="other.xsd#other_TX" '
            'xlink:label="tx"/>'
            "</link:definitionLink></link:linkbase></xs:appinfo></xs:annotation>"
            '<xs:element name="A" id="main_A" substitutionGroup="xbrli:item" '
            'type="xbrli:stringItemType" xbrli:periodType="duration"/>'
            "</xs:schema>"
        )
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "other.xsd").write_text(other)
            (Path(d) / "main.xsd").write_text(main)
            dts = walk(str(Path(d) / "main.xsd"))
            self.assertEqual(len(dts.documents), 2)
            self.assertIn("{http://t.example/other}TX", dts.concepts)
            self.assertEqual(dts.embedded_linkbases, 1)
            self.assertIn("loc", dict(Counter(k for _, k, _ in dts.discovery)))

    def test_json_output_round_trips(self):
        code, out, _ = run_main(str(SCHEMA), "--offline", "--no-cache", "--json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload["concepts"]["total"], 25)


if __name__ == "__main__":
    unittest.main()
