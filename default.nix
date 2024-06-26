with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "sdl-sample";
  src = ./src;
  buildInputs = [ gcc SDL2 SDL2.dev ];
  buildPhase = "c++ -o main physics-test.cpp -lSDL2";

  installPhase = ''
    mkdir -p $out/bin
    cp main $out/bin/
  '';
}