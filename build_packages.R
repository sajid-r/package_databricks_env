# store_packages.R
# stores a list of your currently installed packages

tmp = installed.packages()
installedpackages = as.vector(tmp[is.na(tmp[,"Priority"]), 1])
# save(installedpackages, file="/dbfs/FileStore/tables/installed_R_packages.rda")
# installs each package from the stored list of packages
# load("/dbfs/FileStore/tables/installed_R_packages.rda")

for (count in 1:length(installedpackages)) { 
	download.packages(pkgs = installedpackages[count], destdir = "/dbfs/FileStore/tables/wheelhouse/R", repos='http://cran.us.r-project.org') }