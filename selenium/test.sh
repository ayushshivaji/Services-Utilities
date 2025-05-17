#!/bin/bash


# to get which overlay belongs to which container


df -hT | grep overlay | awk -F '/' '{print $6}' | xargs -I {} bash -c "docker inspect $(docker ps -aq) -f '{{.Name}}: {{.GraphDriver.Data.MergedDir}}' | grep -H {} "


docker inspect $(docker ps -aq)


docker inspect $(docker ps -aq) -f '{{.Name}}: {{.GraphDriver.Data.MergedDir}}' | xargs -n1


docker ps -aq |head  | xargs -I {} bash -c "echo $(docker inspect {} -f '{{.Name}}: {{.GraphDriver.Data.MergedDir}}') $(docker inspect {} -f '{{.GraphDriver.Data.MergedDir}}' | xargs du -sh ) "




docker ps -aq |head  | xargs -I {} sh -c 'for arg do docker inspect "$arg" -f '{{.Name}}: {{.GraphDriver.Data.MergedDir}}'; docker inspect "$arg" -f '{{.GraphDriver.Data.MergedDir}}' | xargs du -sh done;' _


echo "12345" | xargs -d $'\n' sh -c 'for arg do echo "$arg" ; echo "2 $arg" ; done' _
