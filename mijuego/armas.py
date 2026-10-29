D = "src/samples/SDL2/SDL2/"

def rep(fn, old, new):
    s = open(D + fn).read()
    assert s.count(old) == 1, "NO ENCUENTRO en " + fn + ": " + old
    open(D + fn, "w").write(s.replace(old, new))

# ---------- Projectile ----------
rep("Projectile.h", "std::tuple<int, int> GetProjectileLocation();", """std::tuple<int, int> GetProjectileLocation();

    int tinte = 0;
    float guia = 0.0f;""")

rep("Projectile.cpp", "this->currentDest.x = locationX;", """this->verticalSlope = false;
    this->currentDest.x = locationX;""")

rep("Projectile.cpp", "SDL_RenderCopyEx(renderer, this->texture, NULL, &this->currentDest,", """int cr = 255, cg = 255, cb = 255;
        if (this->tinte == 0) { cr = 120; cg = 180; cb = 255; }
        else if (this->tinte == 1) { cr = 255; cg = 130; cb = 60; }
        else if (this->tinte == 2) { cr = 230; cg = 80; cb = 255; }
        else if (this->tinte == 3) { cr = 80; cg = 255; cb = 120; }
        else if (this->tinte == 4) { cr = 255; cg = 230; cb = 60; }
        else if (this->tinte == 5) { cr = 255; cg = 60; cb = 60; }
        else if (this->tinte == 9) { cr = 160; cg = 255; cb = 170; }
        SDL_SetTextureColorMod(this->texture, cr, cg, cb);

        SDL_RenderCopyEx(renderer, this->texture, NULL, &this->currentDest,""")

# ---------- Game.cpp: variables ----------
rep("Game.cpp", "int tickNow = 0;", """int tickNow = 0;

int armaActual = 0;
int armaListoEn = 0;
int armaEspera[6] = { 0, 100, 120, 700, 900, 2500 };
bool armaTengo[6] = { true, true, true, true, true, true };
std::vector<std::pair<int, int>> fragmentos;""")

rep("Game.cpp", "// Reset stats", """// Reset stats
                armaActual = 0;
                armaListoEn = 0;
                fragmentos.clear();""")

# ---------- cambiar de arma ----------
rep("Game.cpp", "// Shield", """// Weapon switch
    case PAD_BUTTON_R1:
        {
            do { armaActual = (armaActual + 1) % 6; } while (!armaTengo[armaActual]);
        }
        break;

    case PAD_BUTTON_L1:
        {
            do { armaActual = (armaActual + 5) % 6; } while (!armaTengo[armaActual]);
        }
        break;

    // Shield""")

# ---------- disparo segun el arma ----------
rep("Game.cpp", "// Create the projectile and add it to the list", """if (tickNow < armaListoEn)
                break;

            armaListoEn = tickNow + armaEspera[armaActual];

            // Create the projectile and add it to the list""")

rep("Game.cpp", "projectiles.push_back(projectile);", """int trayectoria = player->GetTrajectory();

            projectile->tinte = armaActual;
            projectile->guia = (float)trayectoria;

            if (armaActual == 1)
            {
                float rad = trayectoria * 3.14159f / 180.0f;
                int ox = (int)(cosf(rad) * 18.0f);
                int oy = (int)(sinf(rad) * 18.0f);

                projectile->SetLocation(playerX - ox, playerY - oy);

                Projectile* extra = new Projectile(renderer);
                extra->SetTrajectory(trayectoria);
                extra->SetLocation(playerX + ox, playerY + oy);
                extra->tinte = 1;
                projectiles.push_back(extra);
            }

            if (armaActual == 2)
            {
                for (int k = -1; k <= 1; k += 2)
                {
                    Projectile* extra = new Projectile(renderer);
                    extra->SetTrajectory(trayectoria + k * 15);
                    extra->SetLocation(playerX, playerY);
                    extra->tinte = 2;
                    projectiles.push_back(extra);
                }
            }

            projectiles.push_back(projectile);""")

# ---------- efectos al golpear ----------
rep("Game.cpp", "// Increase score", """if (projectile->tinte == 3)
                        fragmentos.push_back(std::make_pair(std::get<0>(projectileCoordinates), std::get<1>(projectileCoordinates)));

                    if (projectile->tinte == 4)
                        enemy->hp -= 1;

                    if (projectile->tinte == 5)
                        enemy->hp -= 3;

                    // Increase score""")

rep("Game.cpp", "checkCollisionUpdates();", """checkCollisionUpdates();

        for (auto& f : fragmentos)
        {
            for (int a = 0; a < 360; a += 36)
            {
                Projectile* frag = new Projectile(renderer);
                frag->SetTrajectory(a);
                frag->SetLocation(f.first, f.second);
                frag->tinte = 9;
                projectiles.push_back(frag);
            }
        }

        fragmentos.clear();""")

# ---------- misiles guiados ----------
rep("Game.cpp", "// Run projectile update", """// Misiles guiados
        for (auto p : projectiles)
        {
            if (p->tinte != 4)
                continue;

            auto pc = p->GetProjectileLocation();
            int px = std::get<0>(pc);
            int py = std::get<1>(pc);

            if (px < 0 || py < 0)
                continue;

            Enemy* objetivo = nullptr;
            float mejor = 1.0e12f;

            for (auto e : enemies)
            {
                auto el = e->GetEnemyLocation();
                float ex = (float)(std::get<0>(el) - px);
                float ey = (float)(std::get<1>(el) - py);
                float d2 = ex * ex + ey * ey;

                if (d2 < mejor)
                {
                    mejor = d2;
                    objetivo = e;
                }
            }

            if (objetivo == nullptr)
                continue;

            auto ol = objetivo->GetEnemyLocation();
            float dx = (float)(std::get<0>(ol) - px);
            float dy = (float)(std::get<1>(ol) - py);
            float deseado = atan2f(dy, dx) * 180.0f / 3.14159f + 90.0f;

            float delta = deseado - p->guia;
            while (delta > 180.0f)
                delta -= 360.0f;
            while (delta < -180.0f)
                delta += 360.0f;

            if (delta > 7.0f)
                delta = 7.0f;
            if (delta < -7.0f)
                delta = -7.0f;

            p->guia += delta;
            p->SetTrajectory((int)p->guia);
            p->SetLocation(px, py);
        }

        // Run projectile update""")

# ---------- escudo burbuja ----------
rep("Game.cpp", "bool apagado = (restante < 1000) && (((tickNow / 100) % 2) == 0);", """bool apagado = (restante < 1000) && (((tickNow / 100) % 2) == 0);

        static SDL_Texture* escudoTex = nullptr;
        static bool escudoIntento = false;

        if (!escudoIntento)
        {
            escudoIntento = true;
            SDL_Surface* es = IMG_Load("/app0/assets/images/escudo.tga");

            if (es != nullptr)
            {
                escudoTex = SDL_CreateTextureFromSurface(renderer, es);
                SDL_FreeSurface(es);

                if (escudoTex != nullptr)
                    SDL_SetTextureBlendMode(escudoTex, SDL_BLENDMODE_BLEND);
            }
        }

        if (escudoTex != nullptr)
        {
            if (!apagado)
            {
                int ew = 0;
                int eh = 0;
                SDL_QueryTexture(escudoTex, NULL, NULL, &ew, &eh);

                SDL_SetTextureAlphaMod(escudoTex, 215 + (int)(40.0f * sinf(tickNow * 0.008f)));

                SDL_Rect ed = { 960 - ew / 2, 540 - eh / 2, ew, eh };
                SDL_RenderCopy(renderer, escudoTex, NULL, &ed);
            }

            apagado = true;
        }""")

# ---------- HUD de armas ----------
rep("Game.cpp", "SDL_Rect fondo = { 1480, 40, 360, 28 };", """int colArma[6][3] = {
        { 80, 160, 255 }, { 255, 130, 60 }, { 230, 80, 255 },
        { 80, 255, 120 }, { 255, 230, 60 }, { 255, 60, 60 }
    };

    for (int i = 0; i < 6; i++)
    {
        SDL_Rect w = { 1480 + i * 44, 148, 36, 24 };

        if (!armaTengo[i])
            SDL_SetRenderDrawColor(renderer, 50, 50, 50, 255);
        else
            SDL_SetRenderDrawColor(renderer, colArma[i][0], colArma[i][1], colArma[i][2], 255);

        SDL_RenderFillRect(renderer, &w);

        if (i == armaActual)
        {
            SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
            SDL_Rect b1 = { w.x - 3, w.y - 3, w.w + 6, 3 };
            SDL_Rect b2 = { w.x - 3, w.y + w.h, w.w + 6, 3 };
            SDL_Rect b3 = { w.x - 3, w.y, 3, w.h };
            SDL_Rect b4 = { w.x + w.w, w.y, 3, w.h };
            SDL_RenderFillRect(renderer, &b1);
            SDL_RenderFillRect(renderer, &b2);
            SDL_RenderFillRect(renderer, &b3);
            SDL_RenderFillRect(renderer, &b4);
        }
    }

    SDL_Rect fondo = { 1480, 40, 360, 28 };""")

print("ARMAS APLICADAS")
