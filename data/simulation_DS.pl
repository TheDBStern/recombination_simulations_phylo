#!/usr/bin/perl

print "Hello, World...\n";
use Cwd;
$dir=getcwd();
$totaldepth=1;
while ($totaldepth<=10) {
	$ind=1;
	while ($ind<=27) {
		&submain;
		$ind *=3;
	}
	$totaldepth +=9;
}

sub submain{
#print STDOUT "Enter the total tree depth, in unit of N generation:\n";
#$totaldepth=<STDIN>;
#chomp($totaldepth);
$depth=$totaldepth/4;
#print STDOUT "Enter the number of individual per species:\n";
#$ind=<STDIN>;
#chomp($ind);
if ($ind==1) {$loci=20;
}elsif ($ind==3){$loci=20;
}elsif ($ind==9){$loci=20;
}elsif ($ind==27){$loci=20;
}else{
die "wrong number of individuals\n";}
$rep=1;
$rate=0.01;
print STDOUT "Change the name of species tree file to 50speciesTrees.nex, press Enter to continue\n";
#<STDIN>;
$speciestree_file="50speciesTrees\.nex";
open ST, "<$speciestree_file" or die "CANNOT find species tree file!\n";
$genealogy=$totaldepth."Ne_".$ind."Ind";
`mkdir $genealogy`;
$speciestree=1;
while ($speciestree<=50) {$tree=<ST>;
	&speciestree;
	$genealogy_file=$genealogy."_ST".$speciestree;
	$sequence_file=$genealogy_file."_Seq";         
	$genealogy_file .= "_G";                       
	$speciestree +=1;                              
	&ms;                                           
	&seqgene;                                      
}
sub ms {
	my $total=$ind*8;
	my $nodeT0=$nodeT[0];
	my $nodeT1=$nodeT[1];
	my $nodeT2=$nodeT[2];
	my $nodeT3=$nodeT[3];
	my $nodeT4=$nodeT[4];
	my $nodeT5=$nodeT[5];
	my $nodeT6=$nodeT[6];
	my $nodeO0=$nodeO[0];
	my $nodeO1=$nodeO[1];
	my $nodeO2=$nodeO[2];
	my $nodeO3=$nodeO[3];
	my $nodeO4=$nodeO[4];
	my $nodeO5=$nodeO[5];
	my $nodeO6=$nodeO[6];
	my $nodeN0=$nodeN[0];
	my $nodeN1=$nodeN[1];
	my $nodeN2=$nodeN[2];
	my $nodeN3=$nodeN[3];
	my $nodeN4=$nodeN[4];
	my $nodeN5=$nodeN[5];
	my $nodeN6=$nodeN[6];
#	print STDOUT "ms $total $loci -T -I 8 $ind $ind $ind $ind $ind $ind $ind $ind -ej $nodeT0 $nodeN0 $nodeO0 -ej $nodeT1 $nodeN1 $nodeO1 -ej $nodeT2 $nodeN2 $nodeO2  -ej $nodeT3 $nodeN3 $nodeO3 -ej $nodeT4 $nodeN4 $nodeO4 -ej $nodeT5 $nodeN5 $nodeO5 -ej $nodeT6 $nodeN6 $nodeO6 | tail +4 |grep -v // >$genealogy_file\n";


`ms $total $loci -T -r 10 1000 -I 8 $ind $ind $ind $ind $ind $ind $ind $ind -ej $nodeT0 $nodeN0 $nodeO0 -ej $nodeT1 $nodeN1 $nodeO1 -ej $nodeT2 $nodeN2 $nodeO2  -ej $nodeT3 $nodeN3 $nodeO3 -ej $nodeT4 $nodeN4 $nodeO4 -ej $nodeT5 $nodeN5 $nodeO5 -ej $nodeT6 $nodeN6 $nodeO6 | tail +4 | grep -v // >$dir/$genealogy/$genealogy_file`;
}
}
sub speciestree {
		undef @nodeT;
		undef @nodeO;
		undef @nodeN;
		$tree =~ s/^.*= \(/\(/;

		while ($tree =~ s/\((\d):(\d+\.*\d*),(\d):(\d+\.*\d*)\):(\d+\.*\d*)/$1:$2+$5/) {
			my $new= $2+$5;
			my $length= $2*$depth/1000;
			push(@nodeO, $1);
			push(@nodeN, $3);
			push(@nodeT, $length);
			$tree =~ s/:(\d+\.*\d*)\+(\d+\.*\d*)/:$new/;

		}
		$tree =~ s/\((\d):(\d+\.*\d*),(\d):(\d+\.*\d*)\)/finish/;
		my $length= $2*$depth/1000;

		push(@nodeO, $1);
		push(@nodeN, $3);
		push(@nodeT, $length);
}

sub seqgene {
	my $randseed=int(rand(999999999));
	`seq-gen -mHKY -l1000 -n$rep -z $randseed -s $rate -p 500 -a0.8 -g4 -f0.3 0.2 0.3 0.2 -t3.0 -on <$dir/$genealogy/$genealogy_file >$dir/$genealogy/$sequence_file`; ####

}