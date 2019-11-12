{ nixpkgs ? import <nixpkgs> {} }:
let
  pkgs_source = fetchTarball https://github.com/NixOS/nixpkgs/archive/19.09.tar.gz;
  # pkgs_source = fetchTarball https://github.com/NixOS/nixpkgs-channels/archive/nixos-unstable.tar.gz;
   overlays = [
      (self: super:                   # define our local packages (useful to fix versions)
         {
          python3 = super.python36.override {
           packageOverrides = python-self: python-super: {
             stanfordnlp = python-self.callPackage ./stanfordnlp-0.2.0.nix { };
           };};})
   ];
   pkgs = import pkgs_source {inherit overlays; };
   py = pkgs.python3;
   myWerkzeug = py.pkgs.werkzeug.overrideAttrs (oldAttrs: rec {
     postPatch = ''
       substituteInPlace werkzeug/_reloader.py \
           --replace "rv = [sys.executable]" "return sys.argv"
             '';
     doCheck = false;
   });

   pyEnv = py.buildEnv.override {
     extraLibs = with py.pkgs;
       [pytorch
         # nltk
        # notebook
        # myWerkzeug
        flask
        stanfordnlp
         # graphviz
         # If you want to have a local virtualenv, see here: https://github.com/NixOS/nixpkgs/blob/master/doc/languages-frameworks/python.section.md
         # scikitlearn
         # notebook
         # etc
        ];
      ignoreCollisions = true;};
in
  pkgs.stdenv.mkDerivation {
    name = "sh-env";
    buildInputs = [pyEnv];
    shellHook = ''
      export LC_ALL=C.UTF-8
      export LANG=C.UTF-8
      export PYTHONIOENCODING=UTF-8
     '';
  }
