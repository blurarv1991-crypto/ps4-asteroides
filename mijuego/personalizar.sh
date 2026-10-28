D=src/samples/SDL2/SDL2
sed -i 's/Score: /Puntos: /g' $D/*.cpp
sed -i 's/Game Over!/Fin del juego/' $D/HUD.cpp
sed -i 's/Press start to restart/Pulsa OPTIONS para reiniciar/' $D/HUD.cpp
sed -i 's/(Difficulty: /(Dificultad: /' $D/HUD.cpp
sed -i 's/"Intermediate"/"Intermedio"/; s/"Hard"/"Dificil"/; s/"Very Hard"/"Muy dificil"/; s/"Death"/"Muerte"/' $D/Game.h
sed -i 's/"Easy"/"Facil"/' $D/Game.cpp
F=0.7 perl -pi -e 's/moveSpeed = ([0-9.]+);/"moveSpeed = ".($1*$ENV{F}).";"/e' $D/Enemy.cpp
python3 mijuego/jefe.py
grep -n "Puntos\|Fin del\|Pulsa\|Dificultad" $D/HUD.cpp
grep -n "Facil" $D/Game.cpp
grep -n "Intermedio\|Dificil\|Muerte" $D/Game.h
grep -n "moveSpeed =" $D/Enemy.cpp
grep -n "bossActive" $D/Game.cpp
