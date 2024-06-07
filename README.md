# Render96ex
This is a fork of [render96ex](https://github.com/Render96/Render96ex)

It has been modified to allow the build of the binary without extracting the assets (see commits [6b80638](https://github.com/cdeletre/Render96ex/commit/6b806380d32e22b2fa1107040b9f0953ef514004), [a1a5adc](https://github.com/cdeletre/Render96ex/commit/a1a5adc15dd54a9d35f2271b222b5bcc4a089931) and [489ebc4](https://github.com/cdeletre/Render96ex/commit/489ebc46eec6261c8b902b2ac55e483e0c098a48))

Also other changes have been done:
- auto detection of audio format for Dynos ([8a81e7e](https://github.com/cdeletre/Render96ex/commit/8a81e7e2f230f48771f7b3c7ad4c023c93efca47))
- force use of timer sync instead of SDL GL Swap Interval ([5b2b30f](https://github.com/cdeletre/Render96ex/commit/5b2b30f3cd8d1b7b7c4478aba166e3d2d7cca5e4)). This is a workaround for the issue [110](https://github.com/Render96/Render96ex/issues/110) presents in some specific configurations.

Only arm64 build has been tested. It is assumed that you can use docker and have the basic knowledges of linux shell.


# Build
## Download sources and checkout the tester_rt64alpha branch

```
git clone https://github.com/cdeletre/Render96ex.git
cd Render96ex
git checkout tester_rt64alpha
```

## Build docker image arm64
This image is needed to build the arm64 binary (EXE)

```
docker build --platform=linux/arm64 . -t render96builder:arm64
```

## Build docker image amd64 (optionnal)
This image is needed if you want to speed up asset extraction on an amd64 computer

```
docker build --platform=linux/amd64 . -t render96builder:amd64
```

## Build binary (EXE) using docker image (arm64)

```
docker run --rm -v ${PWD}:/render96 render96builder:arm64 make NOEXTRACT=1 -j4
```

## Install the binary (EXE)

```
mkdir render96 
cp build/us_pc/sm64.us.f3dex2e render96
```

## Clear build

If you need to restart from scratch.
```
docker run --rm -v ${PWD}:/render96 render96builder:arm64 make distclean
```

Note: it states that `cp: cannot stat './assets/demos/*': No such file or directory`. It needs to be fixed in `Makefile` but it is not a priority as it has no impact.


## Extract assets from the rom

### using docker image (arm64)

```
docker run --rm -v ${PWD}:/render96 render96builder:arm64 make res
```

Note: if you are extracting the assets on amd64 computer it's better to use the amd64 image

### using docker image (amd64)

```
docker run --rm -v ${PWD}:/render96 render96builder:amd64 make res
```

## Install assets

```
cp -R build/us_pc/dynos render96/
cp -R build/us_pc/res render96/
```

# RENDER96-HD-TEXTURE-PACK

## Resized HD texture pack (227 MB)

For system with low memory capacity and/or low resolution display you can use the 25% resized texture pack. In this pack a 256x256 texture is resized to 64x64. It's uses 60% less memory but gives good results on 640x480 displays.

Just download [RENDER96-HD-TEXTURE-PACK-1.2.1-resized.zip](https://raw.githubusercontent.com/cdeletre/Render96ex/tester_rt64alpha/lowmem-packs/RENDER96-HD-TEXTURE-PACK-1.2.1-resized.zip) unzip it and put the folder `gfx` as it into `render96/res`.

### Manual build

If you want to tune the texture pack you can build it from the orignal full sized texture pack available here [https://github.com/pokeheadroom/RENDER96-HD-TEXTURE-PACK](https://github.com/pokeheadroom/RENDER96-HD-TEXTURE-PACK/releases)

```
wget -O RENDER96-HD-TEXTURE-PACK-1.2.1.zip https://codeload.github.com/pokeheadroom/RENDER96-HD-TEXTURE-PACK/zip/refs/tags/1.2.1
unzip RENDER96-HD-TEXTURE-PACK-1.2.1.zip
cp ./Render96ex/tools/resize-textures.sh ./RENDER96-HD-TEXTURE-PACK-1.2.1/
cd RENDER96-HD-TEXTURE-PACK-1.2.1
./resize-textures.sh gfx
```

## Full sized HD texture pack (555 MB)

Just download [RENDER96-HD-TEXTURE-PACK-1.2.1.zip](https://github.com/pokeheadroom/RENDER96-HD-TEXTURE-PACK/archive/refs/tags/1.2.1.zip) unzip it and put the folder `gfx` as it into `render96/res`.

# Dynos packs
## Full size audio pack (403 MB)

This pack is the default audio pack in `dynos/audio`. It's about 403 MB.

## Resampled audio pack (221 MB)

For system with low memory capacity and/or low resolution display you can use resampled audio pack. It uses 22050 Hz audio instead of 44100/32000 Hz (stereo is kept). It uses 44% less memory and still sounds good.

Just copy the `audio` folder from `lowmem/Dynos-audiopack-22050` into `render96/dynos`. You may have to delete the already existing `audio` folder that comes with the initial asset extraction.

## Full size Render96 modelpack 3.2 (64 MB)
Just download [Render96_DynOs_v3.2.7z](https://github.com/Render96/ModelPack/releases/download/3.2/Render96_DynOs_v3.2.7z) unzip it and put the folder `Render96_DynOs_v3.2` into `render96/dynos/packs`.

## Resized Render96 modelpack alpha 3.1 (32 MB)

For system with low memory capacity and/or low resolution display you can use the 25% resized model pack. In this pack a 256x256 texture is resized to 64x64. It's uses 50% less memory but gives good results on 640x480 displays.

Just download [Dynos-Render96-Alpha-3.1-modelpack-resized.zip](https://raw.githubusercontent.com/cdeletre/Render96ex/tester_rt64alpha/lowmem-packs/Dynos-Render96-Alpha-3.1-modelpack-resized.zip
) unzip it and put the folder `audio` into `render96/dynos`. You may have to delete the already existing `audio` folder that comes with the initial asset extraction.

### Manual build

Will be added later. Main steps are:

1. Get modelpack source (PNG, *.c and *.h)
2. Resize and/or edit the textures
3. Copy the modelpack into `render96/dynos/packs`
4. Run the application
5. Wait while it is building the models ( bin files)
6. Exit the application
7. Keep only bin files (remove PNG, *.c and *.h)

This can not be performed with low memory ressource.