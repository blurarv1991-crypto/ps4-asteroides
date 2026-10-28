import re
D = "src/samples/SDL2/SDL2/"
def rep(fn, old, new):
    s = open(D + fn).read()
    assert s.count(old) == 1, "NO ENCUENTRO en " + fn + ": " + old
    open(D + fn, "w").write(s.replace(old, new))

rep("Game.cpp", "bool bossActive = false;", """bool bossActive = false;

int playerHealth = 100;
int playerLives = 4;

struct Particula
{
    float x, y, vx, vy;
    int vida, total, size;
    Uint8 r, g, b;
};
std::vector<Particula> particulas;""")

rep("Game.cpp", "// Reset stats", """// Reset stats
                playerHealth = 100;
                playerLives = 4;
                particulas.clear();""")

rep("Game.cpp", "void checkCollisionUpdates()", """void explosion(int cx, int cy, int cantidad, float vel, int size)
{
    if (particulas.size() > 500)
        return;

    for (int i = 0; i < cantidad; i++)
    {
        float ang = (rand() % 360) * 3.14159f / 180.0f;
        float v = vel * (0.3f + (rand() % 100) / 100.0f);

        Particula p;
        p.x = (float)cx;
        p.y = (float)cy;
        p.vx = cosf(ang) * v;
        p.vy = sinf(ang) * v;
        p.total = 25 + rand() % 20;
        p.vida = p.total;
        p.size = size;

        int c = rand() % 3;
        if (c == 0) { p.r = 255; p.g = 255; p.b = 200; }
        else if (c == 1) { p.r = 255; p.g = 160; p.b = 0; }
        else { p.r = 255; p.g = 60; p.b = 0; }

        particulas.push_back(p);
    }
}

void herirNave(int dano)
{
    playerHealth -= dano;
    explosion(playerX, playerY, 12, 4.0f, 6);

    if (playerHealth <= 0)
    {
        playerLives--;
        explosion(playerX, playerY, 60, 9.0f, 10);

        if (playerLives <= 0)
        {
            playerLives = 0;
            playerHealth = 0;
            gameOver = true;
            explosion(playerX, playerY, 150, 14.0f, 12);
        }
        else
        {
            playerHealth = 100;
        }
    }
}

void dibujarParticulas(SDL_Renderer* renderer)
{
    for (auto& p : particulas)
    {
        int s = (p.size * p.vida) / p.total;
        if (s < 2)
            s = 2;

        SDL_SetRenderDrawColor(renderer, p.r, p.g, p.b, 255);
        SDL_Rect r = { (int)p.x, (int)p.y, s, s };
        SDL_RenderFillRect(renderer, &r);
    }
}

void dibujarVida(SDL_Renderer* renderer)
{
    SDL_Rect fondo = { 1480, 40, 360, 28 };
    SDL_SetRenderDrawColor(renderer, 70, 70, 70, 255);
    SDL_RenderFillRect(renderer, &fondo);

    int ancho = (356 * playerHealth) / 100;
    if (ancho < 0)
        ancho = 0;

    SDL_Rect barra = { 1482, 42, ancho, 24 };

    if (playerHealth > 50)
        SDL_SetRenderDrawColor(renderer, 40, 220, 80, 255);
    else if (playerHealth > 25)
        SDL_SetRenderDrawColor(renderer, 240, 200, 0, 255);
    else
        SDL_SetRenderDrawColor(renderer, 230, 40, 40, 255);

    SDL_RenderFillRect(renderer, &barra);

    for (int i = 0; i < 4; i++)
    {
        SDL_Rect v = { 1480 + i * 44, 80, 36, 36 };

        if (i < playerLives)
            SDL_SetRenderDrawColor(renderer, 80, 160, 255, 255);
        else
            SDL_SetRenderDrawColor(renderer, 70, 70, 70, 255);

        SDL_RenderFillRect(renderer, &v);
    }
}

void checkCollisionUpdates()""")

s = open(D + "Game.cpp").read()
patron = r"//\s*Game over, no need to further process collisions\s*gameOver\s*=\s*true;\s*return;"
assert len(re.findall(patron, s)) == 1, "NO ENCUENTRO el choque enemigo-nave"
nuevo = """// El enemigo explota y dana la nave
            auto pos = it->GetEnemyLocation();
            explosion(std::get<0>(pos) + 48, std::get<1>(pos) + 48, 14, 5.0f, 5);

            if (it->scale > 1.0f)
                bossActive = false;

            for (auto e = enemies.begin(); e != enemies.end(); ++e)
            {
                if (*e == it)
                {
                    delete *e;
                    enemies.erase(e);
                    break;
                }
            }

            herirNave(25);
            return;"""
s = re.sub(patron, lambda m: nuevo, s)
open(D + "Game.cpp", "w").write(s)

rep("Game.cpp", "currentScore += 10;", "currentScore += 10;\n                    explosion(std::get<0>(enemyCoordinates) + 48, std::get<1>(enemyCoordinates) + 48, 14, 5.0f, 5);")

rep("Game.cpp", "// Run HUD updates", """for (size_t i = 0; i < particulas.size();)
    {
        particulas[i].x += particulas[i].vx;
        particulas[i].y += particulas[i].vy;
        particulas[i].vx *= 0.96f;
        particulas[i].vy *= 0.96f;
        particulas[i].vida--;

        if (particulas[i].vida <= 0)
            particulas.erase(particulas.begin() + i);
        else
            i++;
    }

    // Run HUD updates""")

rep("Game.cpp", "hud->Render(renderer);", "hud->Render(renderer);\n    dibujarParticulas(renderer);\n    dibujarVida(renderer);")

print("VIDA APLICADA")
