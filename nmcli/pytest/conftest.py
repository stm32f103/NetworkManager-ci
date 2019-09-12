# content of ./test_smtpsimple.py
import pytest

pytest_plugins = ["NMTest","ConnectionNMTest", "HTML", "editor"]

#@pytest.hookimpl(hookwrapper=True)
#def pytest_runtest_makereport(item, call):
#    pytest_html = item.config.pluginmanager.getplugin('html')
#    outcome = yield
#    report = outcome.get_result()
#
#    setattr(item, "result_" + report.when, report)
#    extra = getattr(report, 'extra', [])
#    extra.append(pytest_html.extras.text("xxx", name="xxx"))
#    fail = hasattr(report, 'wasfail')


# order fixtures https://github.com/pytest-dev/pytest/issues/1216

def order_fixtures(metafunc):
    metafunc.fixturenames[:] = []
    orders = {name: getattr(definition[0].func, "order", None)
              for name, definition in metafunc._arg2fixturedefs.items()}
    ordered = {name: getattr(order, "args")[0] for name, order in orders.items() if order}
    unordered = [name for name, order in orders.items() if not order]
    first = {name: order for name, order in ordered.items() if order and order < 0}
    last = {name: order for name, order in ordered.items() if order and order > 0}
    merged = sorted(first, key=first.get) + unordered + sorted(last, key=last.get)
    metafunc.fixturenames.extend(merged)

def pytest_generate_tests(metafunc):
    order_fixtures(metafunc)
