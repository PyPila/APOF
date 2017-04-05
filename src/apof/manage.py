#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "apof.service.settings.development"
    )

    from django.core.management import execute_from_command_line

    is_testing = 'test' in sys.argv

    if is_testing:
        import coverage
        packages = [
            'portal',
            'baskets',
            'restaurants',
            'menus'
        ]
        cov = coverage.coverage(source=packages, omit=['*/tests/*'])
        cov.erase()
        cov.start()

    execute_from_command_line(sys.argv)

    if is_testing:
        cov.stop()
        cov.save()
        cov.report()
