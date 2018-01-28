#ifndef __OUTPUT_H__
#define __OUTPUT_H__


#include <string>
#include <vector>


#include "file.h"
#include "merge.h"
#include "lib/common.h"


namespace output {


void write_species_counts_header(std::vector<file::SpeciesCount> &fileobjects, std::string &output_fp);
void write_completed_counts(common::countvecmap &kmer_db, std::vector<file::SpeciesCount> &species_counts, merge::Bincodes &bincodes, float threshold, float alpha, std::string &output_fp);


} // namespace output


#endif
