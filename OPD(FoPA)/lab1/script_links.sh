cd ~/lab0
chmod u+rwx sneasel7
chmod u+rwx klang0
chmod u+rw feebas5
chmod u+rw unfezant1
chmod u+rw klang0/mankey
chmod u+r klang0/hippowdon
chmod u+r sewaddle6
chmod u+rwx sneasel7/piloswine
chmod u+rwx sneasel7/accelgor


# жесткая ссылка для файла unfezant1 с именем lab0/sneasel7/dusclopsunfezant
ln ~/lab0/unfezant1 ~/lab0/sneasel7/dusclopsunfezant


# символическая ссылка для файла unfezant1 с именем lab0/sneasel7/dusclopsunfezant
ln -sf ~/lab0/unfezant1 ~/lab0/sneasel7/dusclopsunfezant


# копирование содержимое файла unfezant1 в новый файл lab0/klang0/mankeyunfezant
cat ~/lab0/unfezant1 > ~/lab0/klang0/mankeyunfezant
# cp ~/lab0/unfezant1 ~/lab0/klang0/mankeyunfezant
# cp создаст новый файл, -p сохранит время и права


# копирование файла feebas5 в директорию lab0/sneasel7/piloswine
cp ~/lab0/feebas5 ~/lab0/sneasel7/piloswine/
# cat ~/lab0/feebas5 > ~/lab0/sneasel7/piloswine/feebas5


# объеденение содержимого файлов lab0/klang0/mankey, lab0/klang0/hippowdon, в новый файл lab0/feebas5_47
cat ~/lab0/klang0/mankey ~/lab0/klang0/hippowdon > ~/lab0/feebas5_47


# создание символической ссылки c именем Copy_100 на директорию sewaddle6 в каталоге lab0
ln -s ~/lab0/sewaddle6 ~/lab0/Copy_100


# рекурсивное копирование директории sewaddle6 в директорию lab0/sneasel7/accelgor
cp -r ~/lab0/sewaddle6 ~/lab0/sneasel7/accelgor/
