#!/usr/bin/env bash

cp -r ~/mycroft-core/skills/fallback-unknown.mycroftai/vocab/en-us/ ~/mycroft-core/skills/fallback-unknown.mycroftai/vocab/no-no/
cp -r ~/mycroft-core/skills/fallback-unknown.mycroftai/dialog/en-us/ ~/mycroft-core/skills/fallback-unknown.mycroftai/dialog/no-no/
echo "." > ~/mycroft-core/skills/fallback-unknown.mycroftai/dialog/no-no/unknown.dialog

cp -r ~/mycroft-core/skills/mycroft-volume.mycroftai/vocab/en-us/ ~/mycroft-core/skills/mycroft-volume.mycroftai/vocab/no-no/
cp -r ~/mycroft-core/skills/mycroft-volume.mycroftai/dialog/en-us/ ~/mycroft-core/skills/mycroft-volume.mycroftai/dialog/no-no/
echo "." > ~/mycroft-core/skills/mycroft-volume.mycroftai/dialog/no-no/unknown.dialog
