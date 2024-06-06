FROM ubuntu:22.04 as build

RUN apt-get update && \
    apt-get install -y \
        bsdextrautils \
        build-essential \
        git \
        libglew-dev \
        libsdl2-dev \
        python3

RUN mkdir /render96
WORKDIR /render96
ENV PATH="/render96/tools:${PATH}"

CMD echo 'Build binary:     docker run --rm -v ${PWD}:/render96 render96 make NOEXTRACT=1 -j8\n' \
         'Extract assets:   run --rm -v ${PWD}:/render96 render96 make res\n'\
         'See https://github.com/Render96/Render96ex/wiki for more information'
