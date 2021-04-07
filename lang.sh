#!/usr/bin/env bash

cp -r ~/mycroft-core/skills/fallback-unknown.mycroftai/vocab/en-us/ ~/mycroft-core/skills/fallback-unknown.mycroftai/vocab/no-no/
cp -r ~/mycroft-core/skills/fallback-unknown.mycroftai/dialog/en-us/ ~/mycroft-core/skills/fallback-unknown.mycroftai/dialog/no-no/
echo "." > ~/mycroft-core/skills/fallback-unknown.mycroftai/dialog/no-no/unknown.dialog

cp -r ~/mycroft-core/skills/mycroft-volume.mycroftai/vocab/en-us/ ~/mycroft-core/skills/mycroft-volume.mycroftai/vocab/no-no/
cp -r ~/mycroft-core/skills/mycroft-volume.mycroftai/dialog/en-us/ ~/mycroft-core/skills/mycroft-volume.mycroftai/dialog/no-no/
echo "til" > ~/mycroft-core/skills/mycroft-volume.mycroftai/vocab/no-no/To.voc
echo "volum" > ~/mycroft-core/skills/mycroft-volume.mycroftai/vocab/no-no/Volume.voc
echo "sett" > ~/mycroft-core/skills/mycroft-volume.mycroftai/vocab/no-no/Set.voc
cat > ~/mycroft-core/skills/mycroft-volume.mycroftai/vocab/no-no/Level.voc <<- EOM
0
1
2
3
4
5
6
7
8
9
10
11
en
to
tre
fire
fem
seks
sju
åtte
ni
to
elleve
EOM

echo "volum satt til" > ~/mycroft-core/skills/mycroft-volume.mycroftai/dialog/no-no/set.volume.dialog
echo "volum er på høyeste nivå" > ~/mycroft-core/skills/mycroft-volume.mycroftai/dialog/no-no/max.volume.dialog
echo "volum er allerede på høyeste nivå" > ~/mycroft-core/skills/mycroft-volume.mycroftai/dialog/no-no/already.max.volume.dialog
echo "volum er satt til" > ~/mycroft-core/skills/mycroft-volume.mycroftai/dialog/no-no/volume.is.dialog

cat > ~/.mycroft/mycroft.conf <<- EOM
{
  "max_allowed_core_version": 20.8,  
  "lang": "no-no",
  "tts": {
    "module": "google",
    "google": {
      "lang": "no"
    }
  }
}
EOM
