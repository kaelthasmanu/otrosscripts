#! /bin/bash

# recogemos el directorio a recorrer
#DIR=/media/manuel/_home/recuperado/
DIR=/run/media/manuel/_home/recuperado/
#ext=(3gp avi doc docx flv gif iso jpg mkv mov mp3 mp4 mpg ods odt pdf png ppt rar wav webm webp wma wmv)
#ext="3gp doc docx flv gif iso jpg mov mp3 mpg ods odt pdf png ppt rar wav wma wmv"
#ext="doc docx flv gif iso jpg mp3 ods odt pdf png ppt rar"
ext="mp3"
# entramos a él 
cd $DIR
# y llamamos a la función recorrer_directorio pasandole 
# como parámetro el directorio
# la definición de la función

recorrer_directorio()
{
dir=$(dir -1)
for file in $dir;
do
# comprobamos que la cadena no este vacía
  if [ -n $file ]; then
  if [ -d "$file" ]; then

# si es un directorio, accedemos a él, 
# llamamos recursivamente a la función recorrer_directorio
    echo "DIR: " $file
    cd $file
    recorrer_directorio ./
# una vez que hemos terminado, salimos del directorio (IMPORTANTE)
    cd ..
      else
# dividimos la extensión del nombre del fichero y lo mostramos en pantalla
    extension=${file##*.}
    #echo "${ext/$extension}"
    #echo "$extension"
    if [ "${ext/$extension}" = "$ext" ]; then
      echo "rm -rf $file"
      #mv $file /run/media/manuel/_home/recuperado/new/
      #mv $file /media/manuel/_home/Peliculas/
      rm -rf $file
      else
        echo "mv videos"
        #mv $file /media/manuel/_home/Peliculas/
        echo "si esta"
    fi
    #path_and_name=${file%.*}
    #echo "${ext/$extension}"
    #echo "Fichero:$path_and_name"__"."$extension 
  fi;
  fi;
done;
}
recorrer_directorio $DIR
#cd /home/manuel/
#cat ext.txt | sort | uniq > extlisto.txt 

