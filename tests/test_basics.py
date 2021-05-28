from modpath import modpath, modpath_opt, ModpathOptions
import pytest



@pytest.mark.parametrize(
    "src, dest, opts",
    (
        ("foo.jpg", "foo.txt", {"ext": ".txt"}),
        ("foo.tar.gz", "foo.tar.txt", {"ext": ".txt"}),
        ("foo.tar.gz", "foo.txt", {"ext": ".txt", "multidot": True}),
        ("/tmp/foo.jpg", "/tmp/foo.txt", {"ext": ".txt"}),
        ("/tmp/foo.tar.gz", "/tmp/foo.tar.txt", {"ext": ".txt"}),
        ("/tmp/foo.tar.gz", "/tmp/foo.txt", {"ext": ".txt", "multidot": True}),
        ("foo.jpg", "bar.jpg", {"base": "bar"}),
        ("foo.tar.gz", "bar.tar.gz", {"base": "bar"}),
        ("/tmp/foo.jpg", "/tmp/bar.txt", {"base": "bar"}),
    ),
)
def test_modpath_basics(src: str, dest: str, opts: dict):
    result = modpath(src, **opts)
    assert dest == result
