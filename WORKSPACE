workspace(name = "skeleton_environment")

load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_file")
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "io_bazel_rules_go",
    urls = ["https://github.com/bazelbuild/rules_go/releases/download/0.18.2/rules_go-0.18.2.tar.gz"],
    sha256 = "31f959ecf3687f6e0bb9d01e1e7a7153367ecd82816c9c0ae149cd0e5a92bf8c",
)
http_archive(
    name = "bazel_gazelle",
    urls = ["https://github.com/bazelbuild/bazel-gazelle/releases/download/0.17.0/bazel-gazelle-0.17.0.tar.gz"],
    sha256 = "3c681998538231a2d24d0c07ed5a7658cb72bfb5fd4bf9911157c0e9ac6a2687",
)

http_archive(
    name = "io_bazel_rules_docker",
    sha256 = "c9762a675e55a9537e9742be947b7c3a2aea86a85eb42aad053a49eb917f7164",
    strip_prefix = "rules_docker-35c6cbdbd3a8300c3227920ce03e41510f9b7b0a",
    url = "https://github.com/bazelbuild/rules_docker/archive/35c6cbdbd3a8300c3227920ce03e41510f9b7b0a.tar.gz",
)

load("@io_bazel_rules_go//go:deps.bzl", "go_rules_dependencies", "go_register_toolchains")
go_rules_dependencies()
go_register_toolchains()
load("@bazel_gazelle//:deps.bzl", "gazelle_dependencies")
gazelle_dependencies()


git_repository(
    name = "io_bazel_rules_python",
    remote = "https://github.com/bazelbuild/rules_python.git",
    commit = "9bc2cd89f4d342c6dae2ee6fae4861ebbae69f85",  # 2019-04-07
)

# Only needed for PIP support:
load("@io_bazel_rules_python//python:pip.bzl", "pip_repositories")

pip_repositories()


load("//bazel-rules:pip3_repository.bzl", "pip3_requirements_repository")

pip3_requirements_repository(
    name = "server_deps",
    requirements = "//python_server:requirements.txt",
)

load(
    "@io_bazel_rules_docker//python3:image.bzl",
    _py3_image_repos = "repositories",
)

_py3_image_repos()

