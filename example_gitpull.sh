# Script to perform Git Pull on directory where this Script
# is located
# author: slavisa.karalic@gmail.com


DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
GIT=$(which git)
cd $DIR
exec $GIT pull
