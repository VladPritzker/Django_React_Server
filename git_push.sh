#  ./git_push.sh "commit message"
#!/bin/bash

#!/bin/bash
if [ -z "$1" ]; then
    MESSAGE="Automated commit"
else
    MESSAGE="$1"
fi

git add .
git commit -m "$MESSAGE"
git push origin main