import pytest
from datetime import datetime

from py.xml import html, raw
from html import escape

def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting")
    group.addoption(
        "--html",
        action="store",
        dest="htmlpath",
        metavar="path",
        default=None,
        help="create html report file at given path.",
    )

def pytest_configure(config):
    htmlpath = config.getoption("htmlpath")
    if htmlpath:
        if not hasattr(config, "slaveinput"):
            # prevent opening htmlpath on slave nodes (xdist)
            config._html = HTML(htmlpath)
            config.pluginmanager.register(config._html)


def pytest_unconfigure(config):
    html = getattr(config, "_html", None)
    if html:
        del config._html
        config.pluginmanager.unregister(html)

class HTML:
    items = []
    test_reports = {}
    report_filename = ""
    nm_log_data = {}
    main_log_data = {}
    duration = {}
    embed_index = 0
    def __init__(self, report_filename):
        self.report_filename = report_filename


#    @pytest.hookimpl(hookwrapper=True)
#    def pytest_runtest_makereport(item, call):
#        outcome = yield
#        report = outcome.get_result()
#        #report.cls = item.cls

    def pytest_runtest_logreport(self, report):
        id = report.nodeid
        rep = self.test_reports.get(id, [])
        rep.append(report)
        self.test_reports[id] = rep
        if report.when == "teardown":
            with open("/tmp/journal-nm.log", "r") as f:
                self.nm_log_data[id] = f.read()
            with open("/tmp/main-nm.log", "r") as f:
                self.main_log_data[id] = f.read()
            with open("/tmp/test_duration", "r") as f:
                self.duration[id] = f.read()


    def pytest_sessionfinish(self, session):
        t_start = datetime.now()
        out = self._gen_HTML()
        with open(self.report_filename, "w") as report_file:
            report_file.write(out)
        t_end = datetime.now()
        print("\n\nHTML generated in %s" % (t_end - t_start))


    def _gen_HTML(self):
        head = html.head(
            html.meta(charset="utf-8"), html.title("Test Report"),
            html.style(raw(".hover{background-color:#ddd; padding:0.5em;} .hover:hover{background-color:#eee;} .container{margin-left:0.5em;padding:0.5em;}"))
        )

        body = html.body(
            self._get_info(),
            self._get_reports(),
            html.script(raw("function toggleById(id) { var el = document.getElementById(id); if(el.style.display == 'none') {el.style.display = 'block';} else {el.style.display = 'none';}}"))
        )

        doc = html.html(head, body)

        unicode_doc = "<!DOCTYPE html>\n{}".format(doc.unicode(indent=2))

        # Fix encoding issues, e.g. with surrogates
        unicode_doc = unicode_doc.encode("utf-8", errors="xmlcharrefreplace")
        return unicode_doc.decode("utf-8")


    def _get_info(self):
        return html.div("Some general info here " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def _embed(self, data, target, caption):
        target.append(html.u(caption, onclick="toggleById('emb_%d')" % (self.embed_index), style="cursor:pointer;"))
        data_elem = html.tt(id="emb_%d" %(self.embed_index), style="white-space: pre-wrap;")
        data_elem.extend([html.br(), data, html.br()])
        target.extend([data_elem, html.span(" ")])
        self.embed_index += 1

    def _embed_code(self, data, target):
        code_html = html.tt(style="white-space: pre-wrap;")
        for line in data.splitlines():
            if line.startswith("E"):
                code_html.append(html.span(raw(escape(line)), style="color:red;"))
            elif "@pytest" in line:
                continue
            else:
                code_html.append(html.span(raw(escape(line))))
            code_html.append(html.br())
        target.extend([html.br(), html.div(code_html, style="background-color:#eee;")])

    def _get_source_by_location(self, location):
        file, _, module = location
        if file.endswith(".py"):
            file = file.replace(".py","")
        import importlib
        m = importlib.import_module(file)
        for att in module.split("."):
            m = getattr(m, att)
        import inspect
        return inspect.getsource(m)

    def _get_reports(self):
        div = html.div("Results")
        test_index = 0
        for test in self.test_reports:
            test_split = [ t for t in test.split(":") if t and t != "()" ]
            test_name = test_split[-1]
            test_path = ":".join(test_split[:-1])
            test_div = html.div(test_path + ":", onclick="toggleById('test_%d');" % (test_index), style="cursor:pointer;", Class="hover")
            test_div.append(html.strong(test_name))
            test_div.append(html.span(" "))
            div.append(test_div)
            result_div = html.div(id="test_%d" % (test_index), Class="container")
            fail = []
            embeded_code = False
            for rep in self.test_reports[test]:
                if rep.failed:
                    fail.append(rep.when)
                if rep.longrepr:
                    self._embed_code(rep.longreprtext, result_div)
                    embeded_code = True
                # all standard outputs are stored in "teardown" report
                if rep.when == "teardown":
                    # if there was no report, get test source
                    if not embeded_code:
                        self._embed_code(self._get_source_by_location(rep.location), result_div)
                    sec_index = 0
                    result_div.append(html.br())
                    for sec in rep.sections:
                        header, content = sec
                        header = header.replace("Captured ", "")
                        self._embed(data=content, target=result_div, caption=header)
                        sec_index += 1

            test_div.append(html.small(" (%s)" % self.duration[test]))
            self._embed(data=raw(escape(self.main_log_data[test])), target=result_div, caption="MAIN")

            if len(fail) == 0:
                test_div.append(html.span("PASS", style="color:green;"))
            else:
                test_div.append(html.span("FAIL (%s)" % (" ".join(fail)), style="color:red;"))
                self._embed(data=raw(escape(self.nm_log_data[test])), target=result_div, caption="NM")


            div.append(result_div)
            div.append(html.hr())
            test_index += 1
        return div
