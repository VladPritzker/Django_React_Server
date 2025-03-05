#  ./git_push.sh "commit message"
#!/bin/bash

#!/bin/bash
git add .
git commit -m "${1:-'auto commit'}"
git push origin main
git push gitlab main
