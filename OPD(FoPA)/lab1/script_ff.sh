# 1 пункт
# рекурсивный подсчет символов содержимого файлов, оканчивающихся на '1'
# рез в /tmp/результат, ошибки в /tmp/ошибки
cd ~/lab0
mkdir -p tmp
touch /tmp/errors1 /tmp/result1

cd ~
ls -R ~/lab0 2>/tmp/errors1 | grep '1$' 2>>~/lab0/tmp/errors1 |  wc -m >~/lab0/tmp/result1


# 2 пункт
# вывод 4 первых элемента рекурсивного списка имен и атрибутов файлов
# заканчивающихся на 'e',
# список sort по возрастанию даты изм записи о файле, ошибки доступа подавить
cd ~/lab0
#mkdir -p tmp

ls -lR ~/lab0 2>/dev/null | grep 'e$' | sort -k6,8 | head -n 4

