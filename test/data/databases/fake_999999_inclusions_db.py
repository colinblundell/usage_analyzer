{
    'config': {
        'evaluated_repo_root': 'fake',
        'included_files': ['foo/foo.h', 'bar/bar.h'],
        'name': 'fake',
        'repo_root': 'fake'
    },
    'included_to_including': {
        'bar/bar.h': ['foo/foo.h'],
        'foo/foo.h': [
            'abc/abc.h', 'foo/foo_unittest.cc', 'foo/foo.cc', 'bar/bar.h',
            'bar/core.h', 'qux/qux_factory.h', 'qux/qux_unittest.h'
        ]
    },
    'including_to_included': {
        'bar/bar.h': ['foo/foo.h'],
        'qux/qux_factory.h': ['foo/foo.h'],
        'qux/qux_unittest.h': ['foo/foo.h'],
        'abc/abc.h': ['foo/foo.h'],
        'bar/core.h': ['foo/foo.h'],
        'foo/foo.cc': ['foo/foo.h'],
        'foo/foo.h': ['bar/bar.h'],
        'foo/foo_unittest.cc': ['foo/foo.h']
    },
    'repo_commit_date': '2017-11-22',
    'repo_rev': '9999999',
    'timestamp (UTC)': '2017-11-22 17:44:18.528841',
    'usage_analyzer_rev': 'e390ac3'
}
