
cat input16.txt |grep -P '^(?!.*children)|children: 3,' | \

	grep -P '^(?!.*cats)|cats: 7' | \
	grep -P '^(?!.*samoyeds)|samoyeds: 2' | \
	grep -P '^(?!.*pomeranians)|pomeranians: 3' | \
#	grep -P '^(?!.*akitas)|akitas: 0' | \
	grep -P '^(?!.*vizslas)|vizslas: 0' | \
	grep -P '^(?!.*goldfish)|goldfish: 5' | \
	grep -P '^(?!.*trees)|trees: 3' | \
	grep -P '^(?!.*cars)|cars: 2' | \
	grep -P '^(?!.*perfumes)|perfumes: 1' | \

	cat

