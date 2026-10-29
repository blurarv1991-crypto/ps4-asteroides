D = "src/samples/SDL2/SDL2/"

def rep(fn, old, new):
    s = open(D + fn).read()
    assert s.count(old) == 1, "NO ENCUENTRO en " + fn + ": " + old
    open(D + fn, "w").write(s.replace(old, new))

rep("Game.cpp", "int playerHealth = 100;", """int tickNow = 0;
int shieldEnd = 0;
int shieldReady = 0;

int playerHealth = 100;""")

rep("Game.cpp", "// Reset stats", """// Reset stats
                shieldEnd = 0;
                shieldReady = 0;""")

rep("Game.cpp", "// Restart game", """// Shield
    case PAD_BUTTON_SQUARE:
        {
            if (!gameOver && tickNow >= shieldReady)
            {
                shieldEnd = tickNow + 5000;
                shieldReady = shieldEnd + 15000;
            }
        }
        break;

    // Restart game""")

rep("Game.cpp", "playerHealth -= dano;", """if (tickNow < shieldEnd)
        return;

    playerHealth -= dano;""")

rep("Game.cpp", "// Handle input", """tickNow = totalTickCount;

    // Handle input""")

rep("Game.cpp", "SDL_Rect fondo = { 1480, 40, 360, 28 };", """if (tickNow < shieldEnd)
    {
        int restante = shieldEnd - tickNow;
        bool apagado = (restante < 1000) && (((tickNow / 100) % 2) == 0);

        if (!apagado)
        {
            SDL_SetRenderDrawColor(renderer, 80, 200, 255, 255);

            for (int g = 0; g < 360; g += 2)
            {
                float a = g * 3.14159f / 180.0f;
                SDL_Rect pt = { 960 + (int)(cosf(a) * 60.0f) - 2, 540 + (int)(sinf(a) * 60.0f) - 2, 4, 4 };
                SDL_RenderFillRect(renderer, &pt);
            }
        }
    }

    SDL_Rect sfondo = { 1480, 124, 176, 12 };
    SDL_SetRenderDrawColor(renderer, 70, 70, 70, 255);
    SDL_RenderFillRect(renderer, &sfondo);

    float fraccion = 1.0f;
    if (tickNow < shieldEnd)
        fraccion = (float)(shieldEnd - tickNow) / 5000.0f;
    else if (tickNow < shieldReady)
        fraccion = 1.0f - (float)(shieldReady - tickNow) / 15000.0f;

    SDL_Rect sbarra = { 1482, 126, (int)(172 * fraccion), 8 };

    if (tickNow >= shieldReady)
        SDL_SetRenderDrawColor(renderer, 80, 220, 255, 255);
    else if (tickNow < shieldEnd)
        SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
    else
        SDL_SetRenderDrawColor(renderer, 60, 110, 160, 255);

    SDL_RenderFillRect(renderer, &sbarra);

    SDL_Rect fondo = { 1480, 40, 360, 28 };""")

print("ESCUDO APLICADO")
