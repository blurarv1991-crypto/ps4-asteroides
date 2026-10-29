D=src/samples/SDL2/SDL2
sed -i 's/Score: /Puntos: /g' $D/*.cpp
sed -i 's/Game Over!/Fin del juego/' $D/HUD.cpp
sed -i 's/Press start to restart/Pulsa OPTIONS para reiniciar/' $D/HUD.cpp
sed -i 's/(Difficulty: /(/' $D/HUD.cpp
F=0.7 perl -pi -e 's/moveSpeed = ([0-9.]+);/"moveSpeed = ".($1*$ENV{F}).";"/e' $D/Enemy.cpp
python3 mijuego/jefe.py
python3 mijuego/vida.py
python3 mijuego/niveles.py
python3 mijuego/escudo.py
A=src/samples/SDL2/assets/images
S=72
sudo apt-get install -y imagemagick > /dev/null
convert nave.png -background none -rotate 180 -resize ${S}x${S} -compress None tga:$A/player.tga
convert explorador.png -resize ${S}x${S} -compress None tga:$A/enemy.tga
convert interceptor.png -resize ${S}x${S} -compress None tga:$A/interceptor.tga
convert blindado.png -resize ${S}x${S} -compress None tga:$A/blindado.tga
convert atacante.png -resize ${S}x${S} -compress None tga:$A/atacante.tga
convert guardian.png -resize 224x224 -compress None tga:$A/guardian.tga
identify $A/*.tga
grep -n "Puntos\|Fin del\|Pulsa" $D/HUD.cpp
grep -n "SetTipo" $D/Game.cpp
grep -n "shieldEnd" $D/Game.cpp
