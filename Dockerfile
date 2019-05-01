FROM r-base:3.5.3

RUN \
    # install packages dependencies
    apt-get update -yqq && \
    apt-get install -yqq \
        curl \
        git \
        locales \
        python3 \
        python3-distutils \
        python-pip \
        libcurl4-openssl-dev \
        libssl-dev \
        libxml2-dev \
        wget && \
    apt-get clean && \
    \
    # configure locale, see https://github.com/rocker-org/rocker/issues/19
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen en_US.utf8 && \
    /usr/sbin/update-locale LANG=en_US.UTF-8

# set locales
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8

# mount the output volume as persistant
ENV OUTPUT_DIR /data
VOLUME ${OUTPUT_DIR}
# install R packages
RUN R -e 'source("https://bioconductor.org/biocLite.R"); biocLite(); install.packages(c("pkgmaker","stringr")); install.packages("http://cran.us.r-project.org/src/contrib/Archive/rngtools/rngtools_1.2.3.tar.gz", repos=NULL, type="source", lib="/usr/local/lib/R/site-library/"); biocLite(pkgs=c("MutationalPatterns", "TxDb.Hsapiens.UCSC.hg19.knownGene","BSgenome.Hsapiens.UCSC.hg19"))'
RUN R -e "install.packages(c('argparse','RColorBrewer','gridExtra'))"
# install click_signatures
COPY . /code
RUN pip install /code && rm -rf /code

# add entry point
ENTRYPOINT ["click_signatures"]
