#!/usr/bin/env bash
set -eo pipefail
cd "$(dirname "$0")"

docker run --rm --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges \
  --volume cyber-malware-samples:/samples:ro \
  --volume cyber-analysis-tools:/tools:ro \
  --volume "$PWD:/scripts:ro" \
  --volume "$PWD/../infrastructure/windows/media:/media" \
  cyber-windows-vm:local genisoimage -quiet -J -R -V CYBER_US4 \
  -o /media/us4.iso -graft-points \
  Malware.zip=/samples/Waelmeg-056490ff.zip Tools=/tools \
  preparer.cmd=/scripts/preparer.cmd tester.cmd=/scripts/tester.cmd
