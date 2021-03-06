import unittest
import filecmp
import os
from ariba import summary, summary_sample

modules_dir = os.path.dirname(os.path.abspath(summary.__file__))
data_dir = os.path.join(modules_dir, 'tests', 'data')

class TestSummary(unittest.TestCase):
    def test_init(self):
        '''Test init'''
        fofn = os.path.join(data_dir, 'summary_test_init.fofn')
        s = summary.Summary('out', fofn=fofn)
        self.assertEqual(s.filenames, ['file1', 'file2'])
        s = summary.Summary('out', filenames=['file42'])
        self.assertEqual(s.filenames, ['file42'])
        s = summary.Summary('out', fofn=fofn, filenames=['file42'])
        self.assertEqual(s.filenames, ['file42', 'file1', 'file2'])


    def test_determine_cluster_cols(self):
        col_strings = [
            'assembled,match,ref_seq,pct_id,known_var,novel_var',
            'ref_seq,pct_id,known_var,novel_var',
            'assembled,pct_id,known_var,novel_var',
            'assembled',
            '',
            None,
        ]

        expected = [
            {'assembled': True, 'match': True, 'ref_seq': True, 'pct_id': True, 'known_var': True, 'novel_var': True},
            {'assembled': False, 'match': False, 'ref_seq': True, 'pct_id': True, 'known_var': True, 'novel_var': True},
            {'assembled': True, 'match': False, 'ref_seq': False, 'pct_id': True, 'known_var': True, 'novel_var': True},
            {'assembled': True, 'match': False, 'ref_seq': False, 'pct_id': False, 'known_var': False, 'novel_var': False},
            {'assembled': False, 'match': False, 'ref_seq': False, 'pct_id': False, 'known_var': False, 'novel_var': False},
            {'assembled': False, 'match': False, 'ref_seq': False, 'pct_id': False, 'known_var': False, 'novel_var': False},
        ]

        assert len(col_strings) == len(expected)

        for i in range(len(col_strings)):
            self.assertEqual(expected[i], summary.Summary._determine_cluster_cols(col_strings[i]))


    def test_load_input_files(self):
        '''Test _load_input_files'''
        file1 = os.path.join(data_dir, 'summary_test_load_input_files.1.tsv')
        file2 = os.path.join(data_dir, 'summary_test_load_input_files.2.tsv')
        sample1 = summary_sample.SummarySample(file1)
        sample2 = summary_sample.SummarySample(file2)
        sample1.run()
        sample2.run()
        got = summary.Summary._load_input_files([file1, file2], 90)
        expected = {file1: sample1, file2: sample2}
        self.assertEqual(expected, got)

        sample1 = summary_sample.SummarySample(file1, only_clusters={'noncoding1'})
        sample2 = summary_sample.SummarySample(file2, only_clusters={'noncoding1'})
        sample1.run()
        sample2.run()
        expected = {file1: sample1, file2: sample2}
        got = summary.Summary._load_input_files([file1, file2], 90, only_clusters={'noncoding1'})
        self.assertEqual(expected, got)


    def test_gather_unfiltered_output_data(self):
        '''test gather_output_rows_new'''
        infiles = [
            os.path.join(data_dir, 'summary_gather_unfiltered_output_data.in.1.tsv'),
            os.path.join(data_dir, 'summary_gather_unfiltered_output_data.in.2.tsv')
        ]

        expected_all = {
            infiles[0]: {
                'noncoding1': {
                    'summary': {
                        'assembled': 'yes',
                        'known_var': 'yes',
                        'match': 'yes',
                        'novel_var': 'no',
                        'pct_id': '98.33',
                        'ref_seq': 'noncoding_ref1'
                    },
                    'groups': {},
                    'vars': {},
                },
                'noncoding2': {
                    'summary': {
                        'assembled': 'yes',
                        'known_var': 'yes',
                        'match': 'yes',
                        'novel_var': 'no',
                        'pct_id': '98.33',
                        'ref_seq': 'noncoding_ref2'
                    },
                    'groups': {},
                    'vars': {},
                },
                'presence_absence1': {
                    'summary': {
                        'assembled': 'yes',
                        'known_var': 'no',
                        'match': 'yes',
                        'novel_var': 'yes',
                        'pct_id': '98.96',
                        'ref_seq': 'presence_absence_ref1'
                    },
                    'groups': {},
                    'vars': {},
                }
            },
            infiles[1]: {
                'noncoding1': {
                    'summary': {'assembled': 'yes',
                        'known_var': 'yes',
                        'match': 'yes',
                        'novel_var': 'no',
                        'pct_id': '98.33',
                        'ref_seq': 'noncoding_ref1'
                     },
                    'groups': {},
                    'vars': {},
                },
                'noncoding2': {
                    'summary': {
                        'assembled': 'yes',
                        'known_var': 'yes',
                        'match': 'yes',
                        'novel_var': 'no',
                        'pct_id': '98.33',
                        'ref_seq': 'noncoding_ref2'
                    },
                    'groups': {},
                    'vars': {},
                },
                'presence_absence1': {
                    'summary': {
                            'assembled': 'yes',
                            'known_var': 'no',
                            'match': 'yes',
                            'novel_var': 'yes',
                            'pct_id': '98.96',
                            'ref_seq': 'presence_absence1'
                    },
                    'groups': {},
                    'vars': {}
                }
            }
        }

        expected_potential_cols = {
            'noncoding1': {
                'summary': {
                    'assembled',
                    'known_var',
                    'match',
                    'novel_var',
                    'pct_id',
                    'ref_seq'
                },
                'groups': set(),
                'vars': set()
            },
            'noncoding2': {
                'summary': {
                    'assembled',
                    'known_var',
                    'match',
                    'novel_var',
                    'pct_id',
                    'ref_seq'
                },
                'groups': set(),
                'vars': set()
            },
            'presence_absence1': {
                'summary': {
                    'assembled',
                    'known_var',
                    'match',
                    'novel_var',
                    'pct_id',
                    'ref_seq'
                },
                'groups': set(),
                'vars': set()
            }
        }

        s = summary.Summary('out', filenames=infiles)
        s.samples = summary.Summary._load_input_files(infiles, 90)
        s._gather_unfiltered_output_data()
        self.assertEqual(expected_potential_cols, s.all_potential_columns)
        self.assertEqual(expected_all, s.all_data)

        expected_potential_cols['noncoding1']['groups'] = {'id3', 'id1', 'id1.%'}
        expected_potential_cols['noncoding2']['groups'] = {'id2.%', 'id2'}
        expected_all[infiles[0]]['noncoding1']['groups'] = {'id1': 'yes'}
        expected_all[infiles[0]]['noncoding2']['groups'] = {'id2': 'yes_multi_het', 'id2.%': 'NA'}
        expected_all[infiles[1]]['noncoding1']['groups'] = {'id1': 'het', 'id1.%': 80.0, 'id3': 'yes'}
        expected_all[infiles[1]]['noncoding2']['groups'] = {'id2': 'het', 'id2.%': 40.0}
        s = summary.Summary('out', filenames=infiles, show_var_groups=True)
        s.samples = summary.Summary._load_input_files(infiles, 90)
        s._gather_unfiltered_output_data()
        self.assertEqual(expected_potential_cols, s.all_potential_columns)
        self.assertEqual(expected_all, s.all_data)

        expected_potential_cols['noncoding1']['vars'] = {'A14T.%', 'A6G', 'A14T'}
        expected_potential_cols['noncoding2']['vars'] = {'A52T', 'A52T.%', 'A42T'}
        expected_potential_cols['presence_absence1']['vars'] = {'A10V'}

        expected_all[infiles[0]]['noncoding1']['vars'] = {'A14T': 'yes'}
        expected_all[infiles[0]]['noncoding2']['vars'] = {'A42T': 'yes', 'A52T': 'het', 'A52T.%': 40.0}
        expected_all[infiles[0]]['presence_absence1']['vars'] = {'A10V': 'yes'}
        expected_all[infiles[1]]['noncoding1']['vars'] = {'A14T': 'het', 'A14T.%': 80.0, 'A6G': 'yes'}
        expected_all[infiles[1]]['noncoding2']['vars'] = {'A52T': 'het', 'A52T.%': 40.0}
        expected_all[infiles[1]]['presence_absence1']['vars'] = {'A10V': 'yes'}
        s = summary.Summary('out', filenames=infiles, show_var_groups=True, show_vars=True)
        s.samples = summary.Summary._load_input_files(infiles, 90)
        s._gather_unfiltered_output_data()
        self.assertEqual(expected_potential_cols, s.all_potential_columns)
        self.assertEqual(expected_all, s.all_data)


    def test_to_matrix_all_cols(self):
        '''Test _to_matrix all columns'''
        infiles = [
            os.path.join(data_dir, 'summary_to_matrix.1.tsv'),
            os.path.join(data_dir, 'summary_to_matrix.2.tsv')
        ]

        s = summary.Summary('out', filenames=infiles, show_var_groups=True, show_vars=True)
        s.samples = summary.Summary._load_input_files(infiles, 90)
        s._gather_unfiltered_output_data()
        got_phandango_header, got_csv_header, got_matrix = summary.Summary._to_matrix(infiles, s.all_data, s.all_potential_columns, s.cluster_columns)

        expected_phandango_header = ['name', 'noncoding1.assembled:o1', 'noncoding1.match:o1', 'noncoding1.ref_seq:o2', 'noncoding1.pct_id:c1', 'noncoding1.known_var:o1', 'noncoding1.novel_var:o1', 'noncoding1.id1:o1', 'noncoding1.id1.%:c2', 'noncoding1.id3:o1', 'noncoding1.A14T:o1', 'noncoding1.A14T.%:c2', 'noncoding1.A6G:o1', 'noncoding2.assembled:o1', 'noncoding2.match:o1', 'noncoding2.ref_seq:o3', 'noncoding2.pct_id:c1', 'noncoding2.known_var:o1', 'noncoding2.novel_var:o1', 'noncoding2.id2:o1', 'noncoding2.id2.%:c2', 'noncoding2.A42T:o1', 'noncoding2.A52T:o1', 'noncoding2.A52T.%:c2', 'presence_absence1.assembled:o1', 'presence_absence1.match:o1', 'presence_absence1.ref_seq:o4', 'presence_absence1.pct_id:c1', 'presence_absence1.known_var:o1', 'presence_absence1.novel_var:o1', 'presence_absence1.A10V:o1']
        expected_csv_header = ['name', 'noncoding1.assembled', 'noncoding1.match', 'noncoding1.ref_seq', 'noncoding1.pct_id', 'noncoding1.known_var', 'noncoding1.novel_var', 'noncoding1.id1', 'noncoding1.id1.%', 'noncoding1.id3', 'noncoding1.A14T', 'noncoding1.A14T.%', 'noncoding1.A6G', 'noncoding2.assembled', 'noncoding2.match', 'noncoding2.ref_seq', 'noncoding2.pct_id', 'noncoding2.known_var', 'noncoding2.novel_var', 'noncoding2.id2', 'noncoding2.id2.%', 'noncoding2.A42T', 'noncoding2.A52T', 'noncoding2.A52T.%', 'presence_absence1.assembled', 'presence_absence1.match', 'presence_absence1.ref_seq', 'presence_absence1.pct_id', 'presence_absence1.known_var', 'presence_absence1.novel_var', 'presence_absence1.A10V']
        expected_matrix = [
            [infiles[0], 'yes', 'yes', 'noncoding_ref1', '98.33', 'yes', 'no', 'yes', 'NA', 'no', 'yes', 'NA', 'no', 'yes', 'yes', 'noncoding_ref2', '98.33', 'yes', 'no', 'yes_multi_het', 'NA', 'yes', 'het', 40.0, 'yes', 'yes', 'presence_absence_ref1', '98.96', 'no', 'yes', 'yes'],
            [infiles[1], 'yes', 'yes', 'noncoding_ref1', '98.33', 'yes', 'no', 'het', 80.0, 'yes', 'het', 80.0, 'yes', 'yes', 'yes', 'noncoding_ref2', '98.33', 'yes', 'no', 'het', 40.0, 'no', 'het', 40.0, 'yes', 'yes', 'presence_absence1', '98.96', 'no', 'yes', 'yes']
        ]

        self.assertEqual(expected_phandango_header, got_phandango_header)
        self.assertEqual(expected_csv_header, got_csv_header)
        self.assertEqual(expected_matrix, got_matrix)


    def test_to_matrix_with_groups(self):
        '''Test _to_matrix with groups'''
        infiles = [
            os.path.join(data_dir, 'summary_to_matrix.1.tsv'),
            os.path.join(data_dir, 'summary_to_matrix.2.tsv')
        ]

        s = summary.Summary('out', filenames=infiles, show_var_groups=True)
        s.samples = summary.Summary._load_input_files(infiles, 90)
        s._gather_unfiltered_output_data()
        got_phandango_header, got_csv_header, got_matrix = summary.Summary._to_matrix(infiles, s.all_data, s.all_potential_columns, s.cluster_columns)

        expected_phandango_header = ['name', 'noncoding1.assembled:o1', 'noncoding1.match:o1', 'noncoding1.ref_seq:o2', 'noncoding1.pct_id:c1', 'noncoding1.known_var:o1', 'noncoding1.novel_var:o1', 'noncoding1.id1:o1', 'noncoding1.id1.%:c2', 'noncoding1.id3:o1', 'noncoding2.assembled:o1', 'noncoding2.match:o1', 'noncoding2.ref_seq:o3', 'noncoding2.pct_id:c1', 'noncoding2.known_var:o1', 'noncoding2.novel_var:o1', 'noncoding2.id2:o1', 'noncoding2.id2.%:c2', 'presence_absence1.assembled:o1', 'presence_absence1.match:o1', 'presence_absence1.ref_seq:o4', 'presence_absence1.pct_id:c1', 'presence_absence1.known_var:o1', 'presence_absence1.novel_var:o1']
        expected_csv_header = ['name', 'noncoding1.assembled', 'noncoding1.match', 'noncoding1.ref_seq', 'noncoding1.pct_id', 'noncoding1.known_var', 'noncoding1.novel_var', 'noncoding1.id1', 'noncoding1.id1.%', 'noncoding1.id3', 'noncoding2.assembled', 'noncoding2.match', 'noncoding2.ref_seq', 'noncoding2.pct_id', 'noncoding2.known_var', 'noncoding2.novel_var', 'noncoding2.id2', 'noncoding2.id2.%', 'presence_absence1.assembled', 'presence_absence1.match', 'presence_absence1.ref_seq', 'presence_absence1.pct_id', 'presence_absence1.known_var', 'presence_absence1.novel_var']
        expected_matrix = [
            [infiles[0], 'yes', 'yes', 'noncoding_ref1', '98.33', 'yes', 'no', 'yes', 'NA', 'no', 'yes', 'yes', 'noncoding_ref2', '98.33', 'yes', 'no', 'yes_multi_het', 'NA', 'yes', 'yes', 'presence_absence_ref1', '98.96', 'no', 'yes'],
            [infiles[1], 'yes', 'yes', 'noncoding_ref1', '98.33', 'yes', 'no', 'het', 80.0, 'yes', 'yes', 'yes', 'noncoding_ref2', '98.33', 'yes', 'no', 'het', 40.0, 'yes', 'yes', 'presence_absence1', '98.96', 'no', 'yes']
        ]

        self.assertEqual(expected_phandango_header, got_phandango_header)
        self.assertEqual(expected_csv_header, got_csv_header)
        self.assertEqual(expected_matrix, got_matrix)


    def test_to_matrix_with_vars(self):
        '''Test _to_matrix with vars'''
        infiles = [
            os.path.join(data_dir, 'summary_to_matrix.1.tsv'),
            os.path.join(data_dir, 'summary_to_matrix.2.tsv')
        ]

        s = summary.Summary('out', filenames=infiles, show_vars=True)
        s.samples = summary.Summary._load_input_files(infiles, 90)
        s._gather_unfiltered_output_data()
        got_phandango_header, got_csv_header, got_matrix = summary.Summary._to_matrix(infiles, s.all_data, s.all_potential_columns, s.cluster_columns)

        expected_phandango_header = ['name', 'noncoding1.assembled:o1', 'noncoding1.match:o1', 'noncoding1.ref_seq:o2', 'noncoding1.pct_id:c1', 'noncoding1.known_var:o1', 'noncoding1.novel_var:o1', 'noncoding1.A14T:o1', 'noncoding1.A14T.%:c2', 'noncoding1.A6G:o1', 'noncoding2.assembled:o1', 'noncoding2.match:o1', 'noncoding2.ref_seq:o3', 'noncoding2.pct_id:c1', 'noncoding2.known_var:o1', 'noncoding2.novel_var:o1', 'noncoding2.A42T:o1', 'noncoding2.A52T:o1', 'noncoding2.A52T.%:c2', 'presence_absence1.assembled:o1', 'presence_absence1.match:o1', 'presence_absence1.ref_seq:o4', 'presence_absence1.pct_id:c1', 'presence_absence1.known_var:o1', 'presence_absence1.novel_var:o1', 'presence_absence1.A10V:o1']
        expected_csv_header = ['name', 'noncoding1.assembled', 'noncoding1.match', 'noncoding1.ref_seq', 'noncoding1.pct_id', 'noncoding1.known_var', 'noncoding1.novel_var', 'noncoding1.A14T', 'noncoding1.A14T.%', 'noncoding1.A6G', 'noncoding2.assembled', 'noncoding2.match', 'noncoding2.ref_seq', 'noncoding2.pct_id', 'noncoding2.known_var', 'noncoding2.novel_var', 'noncoding2.A42T', 'noncoding2.A52T', 'noncoding2.A52T.%', 'presence_absence1.assembled', 'presence_absence1.match', 'presence_absence1.ref_seq', 'presence_absence1.pct_id', 'presence_absence1.known_var', 'presence_absence1.novel_var', 'presence_absence1.A10V']
        expected_matrix = [
            [infiles[0], 'yes', 'yes', 'noncoding_ref1', '98.33', 'yes', 'no', 'yes', 'NA', 'no', 'yes', 'yes', 'noncoding_ref2', '98.33', 'yes', 'no', 'yes', 'het', 40.0, 'yes', 'yes', 'presence_absence_ref1', '98.96', 'no', 'yes', 'yes'],
            [infiles[1], 'yes', 'yes', 'noncoding_ref1', '98.33', 'yes', 'no', 'het', 80.0, 'yes', 'yes', 'yes', 'noncoding_ref2', '98.33', 'yes', 'no', 'no', 'het', 40.0, 'yes', 'yes', 'presence_absence1', '98.96', 'no', 'yes', 'yes']
        ]

        self.assertEqual(expected_phandango_header, got_phandango_header)
        self.assertEqual(expected_csv_header, got_csv_header)
        self.assertEqual(expected_matrix, got_matrix)


    def test_to_matrix_cluster_only(self):
        '''Test _to_matrix with cluster columns only'''
        infiles = [
            os.path.join(data_dir, 'summary_to_matrix.1.tsv'),
            os.path.join(data_dir, 'summary_to_matrix.2.tsv')
        ]

        s = summary.Summary('out', filenames=infiles)
        s.samples = summary.Summary._load_input_files(infiles, 90)
        s._gather_unfiltered_output_data()
        got_phandango_header, got_csv_header, got_matrix = summary.Summary._to_matrix(infiles, s.all_data, s.all_potential_columns, s.cluster_columns)

        expected_phandango_header = ['name', 'noncoding1.assembled:o1', 'noncoding1.match:o1', 'noncoding1.ref_seq:o2', 'noncoding1.pct_id:c1', 'noncoding1.known_var:o1', 'noncoding1.novel_var:o1', 'noncoding2.assembled:o1', 'noncoding2.match:o1', 'noncoding2.ref_seq:o3', 'noncoding2.pct_id:c1', 'noncoding2.known_var:o1', 'noncoding2.novel_var:o1', 'presence_absence1.assembled:o1', 'presence_absence1.match:o1', 'presence_absence1.ref_seq:o4', 'presence_absence1.pct_id:c1', 'presence_absence1.known_var:o1', 'presence_absence1.novel_var:o1']
        expected_csv_header = ['name', 'noncoding1.assembled', 'noncoding1.match', 'noncoding1.ref_seq', 'noncoding1.pct_id', 'noncoding1.known_var', 'noncoding1.novel_var', 'noncoding2.assembled', 'noncoding2.match', 'noncoding2.ref_seq', 'noncoding2.pct_id', 'noncoding2.known_var', 'noncoding2.novel_var', 'presence_absence1.assembled', 'presence_absence1.match', 'presence_absence1.ref_seq', 'presence_absence1.pct_id', 'presence_absence1.known_var', 'presence_absence1.novel_var']
        expected_matrix = [
            [infiles[0], 'yes', 'yes', 'noncoding_ref1', '98.33', 'yes', 'no', 'yes', 'yes', 'noncoding_ref2', '98.33', 'yes', 'no', 'yes', 'yes', 'presence_absence_ref1', '98.96', 'no', 'yes'],
            [infiles[1], 'yes', 'yes', 'noncoding_ref1', '98.33', 'yes', 'no', 'yes', 'yes', 'noncoding_ref2', '98.33', 'yes', 'no', 'yes', 'yes', 'presence_absence1', '98.96', 'no', 'yes']
        ]

        self.assertEqual(expected_phandango_header, got_phandango_header)
        self.assertEqual(expected_csv_header, got_csv_header)
        self.assertEqual(expected_matrix, got_matrix)


    def test_to_matrix_assembled_only(self):
        '''Test _to_matrix with assembled column only'''
        infiles = [
            os.path.join(data_dir, 'summary_to_matrix.1.tsv'),
            os.path.join(data_dir, 'summary_to_matrix.2.tsv')
        ]

        s = summary.Summary('out', filenames=infiles, cluster_cols='assembled')
        s.samples = summary.Summary._load_input_files(infiles, 90)
        s._gather_unfiltered_output_data()
        got_phandango_header, got_csv_header, got_matrix = summary.Summary._to_matrix(infiles, s.all_data, s.all_potential_columns, s.cluster_columns)

        expected_phandango_header = ['name', 'noncoding1.assembled:o1', 'noncoding2.assembled:o1', 'presence_absence1.assembled:o1']
        expected_csv_header = ['name', 'noncoding1.assembled', 'noncoding2.assembled', 'presence_absence1.assembled']
        expected_matrix = [
            [infiles[0], 'yes', 'yes', 'yes'],
            [infiles[1], 'yes', 'yes', 'yes']
        ]

        self.assertEqual(expected_phandango_header, got_phandango_header)
        self.assertEqual(expected_csv_header, got_csv_header)
        self.assertEqual(expected_matrix, got_matrix)


    def test_filter_matrix_rows(self):
        '''Test _filter_matrix_rows'''
        matrix = [
            ['yes', 'yes'],
            ['yes', 'no'],
            ['no', 'no'],
            ['yes_nonunique', 'no'],
            ['NA', 'no'],
            ['no', 'NA'],
            ['NA', 'NA']
        ]

        expected = [
            ['yes', 'yes'],
            ['yes', 'no'],
            ['yes_nonunique', 'no'],
        ]
        got = summary.Summary._filter_matrix_rows(matrix)
        self.assertEqual(expected, got)


    def test_filter_matrix_columns(self):
        '''Test _filter_matrix_columns'''
        matrix = [
            ['yes', 'yes', 'no', 'yes_nonunique', 'NA', 'no', 'NA'],
            ['yes', 'no', 'no', 'no', 'no', 'NA', 'NA']
        ]
        phandango_header = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7']
        csv_header = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7']

        got_phandago_header, got_csv_header, got_matrix  = summary.Summary._filter_matrix_columns(matrix, phandango_header, csv_header)
        expected_phandango_header = ['p1', 'p2', 'p4']
        expected_csv_header = ['h1', 'h2', 'h4']
        expected_matrix = [
            ['yes', 'yes', 'yes_nonunique'],
            ['yes', 'no', 'no'],
        ]
        self.assertEqual(expected_phandango_header, got_phandago_header)
        self.assertEqual(expected_csv_header, got_csv_header)
        self.assertEqual(expected_matrix, got_matrix)


    def test_add_phandango_colour_columns(self):
        '''Test _add_phandango_colour_columns'''
        header = ['head1', 'head2:o1', 'head3:o1', 'head4', 'head5:o1']
        matrix = [
            ['yes', 'yes', 'yes_nonunique', 'yes', 'no'],
            ['yes', 'yes_nonunique', 'no', 'yes', 'NA'],
            ['yes', 'no', 'NA', 'yes', 'yes'],
            ['yes', 'NA', 'yes', 'yes', 'yes_nonunique'],
        ]

        expected_header = ['head1', 'head2', 'head2:colour', 'head3', 'head3:colour', 'head4', 'head5', 'head5:colour']
        expected_matrix = [
            ['yes', 'yes', '#33a02c', 'yes_nonunique', '#b2df8a', 'yes', 'no', '#fb9a99'],
            ['yes', 'yes_nonunique', '#b2df8a', 'no', '#fb9a99', 'yes', 'NA', '#d3d3d3'],
            ['yes', 'no', '#fb9a99', 'NA', '#d3d3d3', 'yes', 'yes', '#33a02c'],
            ['yes', 'NA', '#d3d3d3', 'yes', '#33a02c', 'yes', 'yes_nonunique', '#b2df8a']
        ]
        got_header, got_matrix = summary.Summary._add_phandango_colour_columns(header, matrix)
        self.assertEqual(expected_header, got_header)
        self.assertEqual(expected_matrix, got_matrix)


    def test_matrix_to_csv(self):
        '''Test _matrix_to_csv'''
        matrix = [
            ['line1_1', 'line1_2'],
            ['line2_1', 'line2_2'],
        ]
        header = ['head1', 'head2']
        tmpfile = 'tmp.test.matrix_to_csv.csv'
        summary.Summary._matrix_to_csv(matrix, header, tmpfile)
        with open(tmpfile) as f:
            got = f.read()

        expected = 'head1,head2\nline1_1,line1_2\nline2_1,line2_2\n'
        self.assertEqual(expected, got)
        os.unlink(tmpfile)


    def test_distance_score_bewteen_values(self):
        '''Test _distance_score_bewteen_values'''
        tests = [
            (('no', 'no'), 0),
            (('no', 'yes'), 1),
            (('no', 'yes_nonunique'), 1),
            (('no', 'fragmented'), 1),
            (('yes', 'no'), 1),
            (('yes', 'yes'), 0),
            (('yes', 'yes_nonunique'), 1),
            (('yes', 'fragmented'), 1),
            (('yes_nonunique', 'no'), 1),
            (('yes_nonunique', 'yes'), 1),
            (('yes_nonunique', 'yes_nonunique'), 0),
            (('yes_nonunique', 'fragmented'), 1),
            (('fragmented', 'no'), 1),
            (('fragmented', 'yes'), 1),
            (('fragmented', 'yes_nonunique'), 1),
            (('fragmented', 'fragmented'), 0),
            (('NA', 'no'), 0),
            (('NA', 'yes'), 1),
            (('NA', 'yes_nonunique'), 1),
            (('NA', 'fragmented'), 1),
        ]

        for (val1, val2), expected in tests:
            self.assertEqual(expected, summary.Summary._distance_score_between_values(val1, val2))
            self.assertEqual(expected, summary.Summary._distance_score_between_values(val2, val1))



    def test_distance_score_between_lists(self):
        '''Test _distance_score_between_lists'''
        list1 = ['NA', 'no', 'yes']
        list2 = ['NA', 'no', 'no']
        self.assertEqual(1, summary.Summary._distance_score_between_lists(list1, list2))


    def test_write_distance_matrix(self):
        '''Test _write_distance_matrix'''
        rows = [
            ['file1', 'no', 'yes', 'no'],
            ['file2', 'yes', 'no', 'yes'],
            ['file3', 'no', 'no', 'yes'],
        ]

        tmp_distances = 'tmp.test.write_distance_matrix.distances'
        summary.Summary._write_distance_matrix(rows, tmp_distances)
        expected = os.path.join(data_dir, 'summary_test_write_distance_matrix.distances')
        self.assertTrue(filecmp.cmp(expected, tmp_distances, shallow=False))
        os.unlink(tmp_distances)


    def test_newick_from_dist_matrix(self):
        '''Test _newick_from_dist_matrix'''
        tmp_tree = 'tmp.test.newick_from_dist_matrix.tre'
        dist_file = os.path.join(data_dir, 'summary_test_newick_from_dist_matrix.distances')
        summary.Summary._newick_from_dist_matrix(dist_file, tmp_tree)
        # the exact ordering of the nodes is not predictable, so we'll trust dendropy
        # and just check that an output file got written
        self.assertTrue(os.path.exists(tmp_tree))
        os.unlink(tmp_tree)

