import re
D = "src/samples/SDL2/SDL2/"

def leer(fn):
    return open(D + fn).read()

def guardar(fn, s):
    open(D + fn, "w").write(s)

def rep(fn, old, new, veces=1):
    s = leer(fn)
    assert s.count(old) == veces, "NO ENCUENTRO en " + fn + ": " + old
    guardar(fn, s.replace(old, new))

def repx(fn, patron, nuevo):
    s = leer(fn)
    assert len(re.findall(patron, s)) == 1, "NO ENCUENTRO (patron) en " + fn + ": " + patron
    guardar(fn, re.sub(patron, lambda m: nuevo, s))

# ---------- Enemy.h ----------
rep("Enemy.h", "int hp = 1;", """int hp = 1;
    int hpMax = 1;
    int tipo = 0;
    int puntos = 10;
    float hitR = 36.0f;
    float velMul = 1.0f;
    float fase = 0.0f;
    bool zigzag = false;
    int lastOffX = 0;
    int lastOffY = 0;

    void SetTipo(SDL_Renderer* renderer, int t);""")

# ---------- Enemy.cpp ----------
rep("Enemy.cpp", "if (this->scale > 1.0f) SDL_SetTextureColorMod(this->texture, 255, 60, 60);", "")

rep("Enemy.cpp", "this->enemyOrientation, NULL, SDL_FLIP_NONE);", """this->enemyOrientation, NULL, SDL_FLIP_NONE);

        if (this->scale > 1.0f && this->hpMax > 1)
        {
            SDL_Rect fondo = { r.x, r.y - 16, r.w, 10 };
            SDL_SetRenderDrawColor(renderer, 50, 50, 50, 255);
            SDL_RenderFillRect(renderer, &fondo);

            int ancho = ((r.w - 4) * this->hp) / this->hpMax;
            if (ancho < 0)
                ancho = 0;

            SDL_Rect barra = { r.x + 2, r.y - 14, ancho, 6 };
            SDL_SetRenderDrawColor(renderer, 230, 50, 50, 255);
            SDL_RenderFillRect(renderer, &barra);
        }""")

rep("Enemy.cpp", "(this->moveSpeed * deltaFrameTicks)", "(this->moveSpeed * this->velMul * deltaFrameTicks)")

rep("Enemy.cpp", "int directionalModifier = 1;", """this->currentDest.x -= this->lastOffX;
    this->currentDest.y -= this->lastOffY;
    this->lastOffX = 0;
    this->lastOffY = 0;

    int directionalModifier = 1;""")

rep("Enemy.cpp", "this->currentDest.y = (int)y;", """this->currentDest.y = (int)y;

    if (this->zigzag)
    {
        this->fase += 0.006f * deltaFrameTicks;
        float pend = this->trackingSlope;
        float norma = sqrtf(1.0f + pend * pend);
        float amp = 45.0f * sinf(this->fase);
        this->lastOffX = (int)(-pend / norma * amp);
        this->lastOffY = (int)(1.0f / norma * amp);
        this->currentDest.x += this->lastOffX;
        this->currentDest.y += this->lastOffY;
    }""")

s = leer("Enemy.cpp")
s += """

void Enemy::SetTipo(SDL_Renderer* renderer, int t)
{
    const char* archivos[5] = {
        "/app0/assets/images/enemy.tga",
        "/app0/assets/images/interceptor.tga",
        "/app0/assets/images/blindado.tga",
        "/app0/assets/images/atacante.tga",
        "/app0/assets/images/guardian.tga"
    };

    if (t < 0 || t > 4)
        t = 0;

    this->tipo = t;

    if (t != 0)
    {
        SDL_Surface* surf = IMG_Load(archivos[t]);

        if (surf != nullptr)
        {
            if (this->texture != nullptr)
                SDL_DestroyTexture(this->texture);

            this->texture = SDL_CreateTextureFromSurface(renderer, surf);
            SDL_FreeSurface(surf);
        }
    }

    int w = 72;
    int h = 72;

    if (this->texture != nullptr)
        SDL_QueryTexture(this->texture, NULL, NULL, &w, &h);

    this->hitR = w * 0.5f;
    this->hp = 1;
    this->hpMax = 1;
    this->velMul = 1.0f;
    this->zigzag = false;
    this->puntos = 10;

    switch (t)
    {
    case 1:
        this->velMul = 1.3f;
        this->zigzag = true;
        this->puntos = 15;
        break;
    case 2:
        this->hp = 3;
        this->hpMax = 3;
        this->puntos = 25;
        break;
    case 3:
        this->hp = 2;
        this->hpMax = 2;
        this->velMul = 1.5f;
        this->puntos = 20;
        break;
    case 4:
        this->velMul = 0.8f;
        this->puntos = 100;
        break;
    default:
        break;
    }
}
"""
guardar("Enemy.cpp", s)

# ---------- Game.h : nombres de nivel ----------
h = leer("Game.h")
for nombre, texto in [("ONE", "Nivel 2"), ("TWO", "Nivel 3"), ("THREE", "Nivel 4"), ("FOUR", "Nivel 5"), ("FIVE", "Final")]:
    patron = r'(#define DIFFICULTY_LEVEL_' + nombre + r'\s+)"[^"]*"'
    assert len(re.findall(patron, h)) == 1, "NO ENCUENTRO define " + nombre
    h = re.sub(patron, lambda m: m.group(1) + '"' + texto + '"', h)
guardar("Game.h", h)

# ---------- Game.cpp ----------
repx("Game.cpp", r'std::string difficultyDisplay = "[^"]*";', 'std::string difficultyDisplay = "Nivel 1";')
rep("Game.cpp", "hud->SetScore(0, DIFFICULTY_LEVEL_ONE);", 'hud->SetScore(0, "Nivel 1");')
repx("Game.cpp", r"currentScore\s*=\s*0;\s*difficultyLevel\s*=\s*LEVEL_ONE;\s*difficultyDisplay\s*=\s*DIFFICULTY_LEVEL_ONE;",
     'currentScore = 0;\n                difficultyLevel = LEVEL_ZERO;\n                difficultyDisplay = "Nivel 1";')

rep("Game.cpp", "int bossAt[5] = { 100, 250, 500, 900, 1400 };", "int bossAt[5] = { 1000, 2000, 3000, 4000, 5000 };")
rep("Game.cpp", "(96 / 2)", "(int)enemy->hitR", 2)
rep("Game.cpp", "currentScore += 10;", "currentScore += enemy->puntos;")

rep("Game.cpp", "enemies.back()->scale = 2.5f;", """int tipoJefe = bossesDefeated;
            if (tipoJefe > 4)
                tipoJefe = 4;

            enemies.back()->SetTipo(renderer, tipoJefe);
            enemies.back()->puntos = 100;
            enemies.back()->scale = (tipoJefe < 4) ? 2.5f : 1.01f;
            enemies.back()->hp = 8 + bossesDefeated * 4;
            enemies.back()->hpMax = enemies.back()->hp;
            enemies.back()->velMul = 0.8f;
            enemies.back()->zigzag = false;
            enemies.back()->hitR = enemies.back()->hitR * enemies.back()->scale;""")
rep("Game.cpp", "enemies.back()->hp = 5 + bossesDefeated * 2;", "")

repx("Game.cpp", r"else if \(!bossActive\)\s*\{\s*spawnEnemy\(renderer\);\s*\}", """else if (!bossActive)
        {
            spawnEnemy(renderer);

            int tipoNormal = bossesDefeated;
            if (tipoNormal >= 4)
                tipoNormal = rand() % 4;

            enemies.back()->SetTipo(renderer, tipoNormal);
        }""")

print("NIVELES APLICADOS")
