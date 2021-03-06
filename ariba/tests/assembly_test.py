import unittest
import sys
import os
import shutil
import filecmp
import pyfastaq
from ariba import assembly

modules_dir = os.path.dirname(os.path.abspath(assembly.__file__))
data_dir = os.path.join(modules_dir, 'tests', 'data')


class TestAssembly(unittest.TestCase):
    def test_get_assembly_kmer(self):
        '''test _get_assembly_kmer'''
        reads1 = os.path.join(data_dir, 'assembly_test_set_assembly_kmer_reads_1.fq')
        reads2 = os.path.join(data_dir, 'assembly_test_set_assembly_kmer_reads_2.fq')
        got = assembly.Assembly._get_assembly_kmer(0, reads1, reads2)
        self.assertEqual(got, 5)
        got = assembly.Assembly._get_assembly_kmer(42, reads1, reads2)
        self.assertEqual(got, 42)


    def _test_check_spades_log_file(self):
        '''_test _check_spades_log_file'''
        good_file = os.path.join(data_dir, 'assembly_test_check_spades_log_file.log.good')
        bad_file = os.path.join(data_dir, 'assembly_test_check_spades_log_file.log.bad')
        self.assertTrue(assembly.Assembly._check_spades_log_file(good_file))
        with self.assertRaises(assembly.Error):
            self.assertTrue(assembly.Assembly._check_spades_log_file(bad_file))


    def test_run_fermilite(self):
        '''test _run_fermilite'''
        reads = os.path.join(data_dir, 'assembly_run_fermilite.reads.fq')
        tmp_fa = 'tmp.test_run_fermilite.fa'
        tmp_log = 'tmp.test_run_fermilite.log'
        expected_fa = os.path.join(data_dir, 'assembly_run_fermilite.expected.fa')
        expected_log = os.path.join(data_dir, 'assembly_run_fermilite.expected.log')
        got = assembly.Assembly._run_fermilite(reads, tmp_fa, tmp_log)
        self.assertEqual(0, got)
        self.assertTrue(filecmp.cmp(expected_fa, tmp_fa, shallow=False))
        self.assertTrue(filecmp.cmp(expected_log, tmp_log, shallow=False))
        os.unlink(tmp_fa)
        os.unlink(tmp_log)


    def test_run_fermilite_fails(self):
        '''test _run_fermilite when it fails'''
        reads = os.path.join(data_dir, 'assembly_run_fermilite_fail.reads.fq')
        tmp_fa = 'tmp.test_run_fermilite_fails.fa'
        tmp_log = 'tmp.test_run_fermilite_fails.log'
        expected_log = os.path.join(data_dir, 'assembly_run_fermilite_fails.expected.log')
        got = assembly.Assembly._run_fermilite(reads, tmp_fa, tmp_log)
        self.assertEqual(1, got)
        self.assertFalse(os.path.exists(tmp_fa))
        self.assertTrue(filecmp.cmp(expected_log, tmp_log, shallow=False))
        os.unlink(tmp_log)


    def test_assemble_with_fermilite(self):
        '''test _assemble_with_fermilite'''
        reads1 = os.path.join(data_dir, 'assembly_assemble_with_fermilite.reads_1.fq')
        reads2 = os.path.join(data_dir, 'assembly_assemble_with_fermilite.reads_2.fq')
        expected_log = os.path.join(data_dir, 'assembly_assemble_with_fermilite.expected.log')
        expected_fa = os.path.join(data_dir, 'assembly_assemble_with_fermilite.expected.fa')
        tmp_dir = 'tmp.test_assemble_with_fermilite'
        tmp_log = 'tmp.test_assemble_with_fermilite.log'
        tmp_log_fh = open(tmp_log, 'w')
        print('First line', file=tmp_log_fh)
        a = assembly.Assembly(reads1, reads2, 'not needed', 'not needed', tmp_dir, 'not_needed_for_this_test.fa', 'not_needed_for_this_test.bam', tmp_log_fh)
        a._assemble_with_fermilite()
        self.assertTrue(a.assembled_ok)
        tmp_log_fh.close()
        self.assertTrue(filecmp.cmp(expected_log, tmp_log, shallow=False))
        self.assertTrue(filecmp.cmp(expected_fa, os.path.join(tmp_dir, 'contigs.fa'), shallow=False))
        shutil.rmtree(tmp_dir)
        os.unlink(tmp_log)


    def test_assemble_with_fermilite_fails(self):
        '''test _assemble_with_fermilite fails'''
        reads1 = os.path.join(data_dir, 'assembly_assemble_with_fermilite_fails.reads_1.fq')
        reads2 = os.path.join(data_dir, 'assembly_assemble_with_fermilite_fails.reads_2.fq')
        expected_log = os.path.join(data_dir, 'assembly_assemble_with_fermilite_fails.expected.log')
        tmp_dir = 'tmp.test_assemble_with_fermilite_fails'
        tmp_log = 'tmp.test_assemble_with_fermilite_fails.log'
        tmp_log_fh = open(tmp_log, 'w')
        print('First line', file=tmp_log_fh)
        a = assembly.Assembly(reads1, reads2, 'not needed', 'not needed', tmp_dir, 'not_needed_for_this_test.fa', 'not_needed_for_this_test.bam', tmp_log_fh)
        a._assemble_with_fermilite()
        self.assertFalse(a.assembled_ok)
        tmp_log_fh.close()
        self.assertTrue(filecmp.cmp(expected_log, tmp_log, shallow=False))
        self.assertFalse(os.path.exists(os.path.join(tmp_dir, 'contigs.fa')))
        shutil.rmtree(tmp_dir)
        os.unlink(tmp_log)


    def test_assemble_with_spades(self):
        '''test _assemble_with_spades'''
        return # but leave code here in case we decide to use spades later
        reads1 = os.path.join(data_dir, 'assembly_test_assemble_with_spades_reads_1.fq')
        reads2 = os.path.join(data_dir, 'assembly_test_assemble_with_spades_reads_2.fq')
        ref_fasta = os.path.join(data_dir, 'assembly_test_assemble_with_spades_ref.fa')
        tmp_dir = 'tmp.test_assemble_with_spades'
        a = assembly.Assembly(reads1, reads2, 'not needed', ref_fasta, tmp_dir, 'not_needed_for_this_test.fa', 'not_needed_for_this_test.bam', sys.stdout)
        a._assemble_with_spades(unittest=True)
        self.assertTrue(a.assembled_ok)
        shutil.rmtree(tmp_dir)


    def test_assemble_with_spades_fail(self):
        '''test _assemble_with_spades handles spades fail'''
        return # but leave code here in case we decide to use spades later
        reads1 = os.path.join(data_dir, 'assembly_test_assemble_with_spades_reads_1.fq')
        reads2 = os.path.join(data_dir, 'assembly_test_assemble_with_spades_reads_2.fq')
        ref_fasta = os.path.join(data_dir, 'assembly_test_assemble_with_spades_ref.fa')
        tmp_dir = 'tmp.test_assemble_with_spades'
        a = assembly.Assembly(reads1, reads2, 'not needed', ref_fasta, tmp_dir, 'not_needed_for_this_test.fa', 'not_needed_for_this_test.bam', sys.stdout)
        a._assemble_with_spades(unittest=False)
        self.assertFalse(a.assembled_ok)
        shutil.rmtree(tmp_dir)


    def test_scaffold_with_sspace(self):
        '''test _scaffold_with_sspace'''
        return # but leave code here in case we decide to use sspace later
        reads1 = os.path.join(data_dir, 'assembly_test_assemble_with_spades_reads_1.fq')
        reads2 = os.path.join(data_dir, 'assembly_test_assemble_with_spades_reads_2.fq')
        ref_fasta = os.path.join(data_dir, 'assembly_test_assemble_with_spades_ref.fa')
        tmp_dir = 'tmp.test_scaffold_with_sspace'
        a = assembly.Assembly(reads1, reads2, 'not needed', ref_fasta, tmp_dir, 'not_needed_for_this_test.fa', 'not_needed_for_this_test.bam', sys.stdout)
        a.assembly_contigs = os.path.join(data_dir, 'assembly_test_scaffold_with_sspace_contigs.fa')
        a._scaffold_with_sspace()
        self.assertTrue(os.path.exists(a.scaffolder_scaffolds))
        shutil.rmtree(tmp_dir)


    def test_has_gaps_to_fill(self):
        '''test _has_gaps_to_fill'''
        return # but leave code here in case we decide to use gapfiller later
        no_gaps = os.path.join(data_dir, 'assembly_test_has_gaps_to_fill.no_gaps.fa')
        has_gaps = os.path.join(data_dir, 'assembly_test_has_gaps_to_fill.has_gaps.fa')
        self.assertTrue(assembly.Assembly._has_gaps_to_fill(has_gaps))
        self.assertFalse(assembly.Assembly._has_gaps_to_fill(no_gaps))


    def test_rename_scaffolds(self):
        '''test _rename_scaffolds'''
        infile = os.path.join(data_dir, 'assembly_test_rename_scaffolds.in.fa')
        outfile = os.path.join(data_dir, 'assembly_test_rename_scaffolds.out.fa')
        tmpfile = 'tmp.fa'
        assembly.Assembly._rename_scaffolds(infile, tmpfile, 'prefix')
        self.assertTrue(filecmp.cmp(outfile, tmpfile, shallow=False))
        os.unlink(tmpfile)


    def test_gap_fill_with_gapfiller_no_gaps(self):
        return # but leave code here in case we decide to use gapfiller later
        '''test _gap_fill_with_gapfiller no gaps'''
        reads1 = os.path.join(data_dir, 'assembly_test_gapfill_with_gapfiller_reads_1.fq')
        reads2 = os.path.join(data_dir, 'assembly_test_gapfill_with_gapfiller_reads_2.fq')
        tmp_dir = 'tmp.gap_fill_with_gapfiller_no_gaps'
        a = assembly.Assembly(reads1, reads2, 'not needed', 'ref.fa', tmp_dir, 'not_needed_for_this_test.fa', 'not_needed_for_this_test.bam', sys.stdout)
        a.scaffolder_scaffolds = os.path.join(data_dir, 'assembly_test_gapfill_with_gapfiller.scaffolds_no_gaps.fa')
        a._gap_fill_with_gapfiller()
        self.assertTrue(os.path.exists(a.gapfilled_scaffolds))
        shutil.rmtree(tmp_dir)


    def test_gap_fill_with_gapfiller_with_gaps(self):
        return # but leave code here in case we decide to use gapfiller later
        '''test _gap_fill_with_gapfiller with gaps'''
        reads1 = os.path.join(data_dir, 'assembly_test_gapfill_with_gapfiller_reads_1.fq')
        reads2 = os.path.join(data_dir, 'assembly_test_gapfill_with_gapfiller_reads_2.fq')
        tmp_dir = 'tmp.gap_fill_with_gapfiller_with_gaps'
        a = assembly.Assembly(reads1, reads2, 'not needed', 'ref.fa', tmp_dir, 'not_needed_for_this_test.fa', 'not_needed_for_this_test.bam', sys.stdout)
        a.scaffolder_scaffolds = os.path.join(data_dir, 'assembly_test_gapfill_with_gapfiller.scaffolds_with_gaps.fa')
        a._gap_fill_with_gapfiller()
        self.assertTrue(os.path.exists(a.gapfilled_scaffolds))
        shutil.rmtree(tmp_dir)


    def test_fix_contig_orientation(self):
        '''test _fix_contig_orientation'''
        scaffs_in = os.path.join(data_dir, 'assembly_test_fix_contig_orientation.in.fa')
        expected_out = os.path.join(data_dir, 'assembly_test_fix_contig_orientation.out.fa')
        ref_fa = os.path.join(data_dir, 'assembly_test_fix_contig_orientation.ref.fa')
        tmp_out = 'tmp.assembly_test_fix_contig_orientation.out.fa'
        got = assembly.Assembly._fix_contig_orientation(scaffs_in, ref_fa, tmp_out)
        expected = {'match_both_strands'}
        self.assertTrue(filecmp.cmp(expected_out, tmp_out, shallow=False))
        self.assertEqual(expected, got)
        os.unlink(tmp_out)


    def test_parse_bam(self):
        '''test _parse_bam'''
        bam = os.path.join(data_dir, 'assembly_test_parse_assembly_bam.bam')
        assembly_fa = os.path.join(data_dir, 'assembly_test_parse_assembly_bam.assembly.fa')
        assembly_seqs = {}
        pyfastaq.tasks.file_to_dict(assembly_fa, assembly_seqs)
        self.assertTrue(assembly.Assembly._parse_bam(assembly_seqs, bam, 10, 1000))
        os.unlink(bam + '.soft_clipped')
        os.unlink(bam + '.unmapped_mates')
        os.unlink(bam + '.scaff')

