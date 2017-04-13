import click


@click.group()
def command():
    pass


@command.command(
    add_help_option=False,
    context_settings={'ignore_unknown_options': True}
)
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def django(context, args):
    from django.core.management import execute_from_command_line
    execute_from_command_line(argv=[context.command_path] + list(args))


@command.command(
    add_help_option=False,
    context_settings={'ignore_unknown_options': True}
)
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def test(context, args):
    import coverage
    cov = coverage.Coverage()
    cov.start()

    context.invoke(django, args=['test'] + list(args))

    cov.stop()
    cov.save()

    cov.html_report()
    cov.report()
