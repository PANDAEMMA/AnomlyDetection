#! /usr/bin/perl -w
#parse the original log to _w.csv,_rw.csv,_r.csv

my $fname ="ktyo.2013";
open(FH1, $fname.".txt") || die "Cannot open: [FileFiles.pl]$!";

while(<FH1>){
	print $_
}
