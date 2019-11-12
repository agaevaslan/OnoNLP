{ buildPythonPackage
, fetchPypi
, tqdm
, requests
, pytorch
, numpy
, protobuf
, lib
}:

buildPythonPackage rec {
  version = "0.2.0";
  pname = "stanfordnlp";

  src = fetchPypi {
    inherit pname version;
    sha256 = "0jcsni8wp5vx18qgxgk0ycj3qmnlpp2rlik1qkhv3jr3xzgmdgd8";
  };

  propagatedBuildInputs = [ tqdm requests pytorch numpy protobuf ];

  # Tests require extra dependencies
  doCheck = false;

  meta = {
    homepage = https://github.com/stanfordnlp/stanfordnlp;
    description = "Official Stanford NLP Python Library for Many Human Languages";
    license = lib.licenses.bsd3;
    maintainers = with lib.maintainers; [ vladmaraev ];
  };
}
