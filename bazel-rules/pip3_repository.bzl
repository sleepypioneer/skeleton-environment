def _pip3_requirements_repository_impl(rctx):
    if not rctx.which("python3"):
        fail("python3 not found")
    if not rctx.which("pip3"):
        fail("pip3 not found")

    rctx.file("BUILD", "")

    req = '''
def requirement(name):
    name_key = name.replace("-", "_").lower()
    return "@%s//" + name_key + ":pkg"
''' % (rctx.attr.name)
    rctx.file("requirements.bzl", req)

    exec_result = rctx.execute(
        [
            "pip3",
            "wheel",
            "-r%s" % rctx.path(rctx.attr.requirements),
        ] + rctx.attr.wheel_args,
        environment = rctx.attr.wheel_env,
    )

    if exec_result.return_code:
        fail("Failed to obtain package wheel: \n%s\n%s" % (exec_result.stdout, exec_result.stderr))
    if exec_result.stderr:
        print(exec_result.stderr)

    exec_result = rctx.execute(["find", ".", "-type", "f", "-name", "*.whl"])
    if exec_result.return_code:
        fail("Could not find package wheel: \n%s" % exec_result.stderr)

    whl_files = exec_result.stdout.rstrip().split("\n")

    for whl_file in whl_files:
        whl_dir = str(whl_file).lower().split("-")[0]
        result = rctx.execute(["mkdir", whl_dir])

        if result.return_code:
            fail("mkdir failed: %s (%s)" % (result.stdout, result.stderr))

        args = [
            "python3",
            rctx.path(rctx.attr._script),
            "--whl",
            whl_file,
            "--requirements",
            "@%s//:requirements.bzl" % rctx.attr.name,
            "--directory",
            whl_dir,
        ]

        if rctx.attr.extras:
            args += [
                "--extras=%s" % extra
                for extra in rctx.attr.extras
            ]
        result = rctx.execute(args)
        if result.return_code:
            fail("whl_library failed: %s (%s)" % (result.stdout, result.stderr))

        rctx.execute(["rm", whl_file])

    return

pip3_requirements_repository = repository_rule(
    attrs = {
        "requirements": attr.label(
            allow_files = True,
            mandatory = True,
            single_file = True,
        ),
        "extras": attr.string_list(),
        "wheel_args": attr.string_list(),
        "wheel_env": attr.string_dict(),
        "_script": attr.label(
            executable = True,
            default = Label("@io_bazel_rules_python//tools:whltool.par"),
            cfg = "host",
        ),
    },
    local = False,
    implementation = _pip3_requirements_repository_impl,
)
