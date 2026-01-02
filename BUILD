genrule(
    name = "see_bin",
    srcs = glob(["app/**/*.py", "doc/**/*.yaml"]),
    outs = ["see"],
    cmd = """
        /opt/homebrew/bin/nuitka \
            --onefile \
            --include-data-dir=doc=doc \
            --onefile-tempdir-spec=/tmp/nuitka-see \
            --no-progressbar \
            --assume-yes-for-downloads \
            --output-dir=$$(dirname $(location see)) \
            --output-filename=see \
            $(location app/main.py)
    """,
    local = 1,
    visibility = ["//visibility:public"],
)
