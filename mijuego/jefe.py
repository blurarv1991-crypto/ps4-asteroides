D = "src/samples/SDL2/SDL2/"
def rep(fn, old, new): s = open(D + fn).read(); assert s.count(old) == 1, "NO ENCUENTRO en " + fn + ": " + old; open(D + fn, "w").write(s.replace(old, new))

rep("Enemy.h", "std::tuple<int, int> GetEnemyLocation();", "std::tuple<int, int> GetEnemyLocation();\n\n    float scale = 1.0f;\n    int hp = 1;")

rep("Enemy.cpp", "SDL_RenderCopyEx(renderer, this->texture, NULL, &this->currentDest,", """SDL_Rect r = this->currentDest;
        r.w = (int)(r.w * this->scale);
        r.h = (int)(r.h * this->scale);
        r.x = this->currentDest.x - (r.w - this->currentDest.w) / 2;
        r.y = this->currentDest.y - (r.h - this->currentDest.h) / 2;
        if (this->scale > 1.0f) SDL_SetTextureColorMod(this->texture, 255, 60, 60);
        SDL_RenderCopyEx(renderer, this->texture, NULL, &r,""")

rep("Game.cpp", "bool gameOver = false;", "bool gameOver = false;\nbool bossActive = false;\nint bossesDefeated = 0;\nint bossAt[5] = { 100, 250, 500, 900, 1400 };")

rep("Game.cpp", "// Reset stats", "// Reset stats\n                bossActive = false;\n                bossesDefeated = 0;")

rep("Game.cpp", "currentScore += 10;", """if (enemy->hp > 1)
                    {
                        enemy->hp--;
                        delete projectile;
                        projectile = nullptr;
                        projectileIt = projectiles.erase(projectileIt);
                        break;
                    }

                    currentScore += 10;

                    if (enemy->scale > 1.0f)
                    {
                        bossActive = false;
                        bossesDefeated++;
                    }""")

rep("Game.cpp", "if (currentScore > 50)", "if (bossesDefeated >= 1)")
rep("Game.cpp", "if (currentScore > 100)", "if (bossesDefeated >= 2)")
rep("Game.cpp", "if (currentScore > 200)", "if (bossesDefeated >= 3)")
rep("Game.cpp", "if (currentScore > 500)", "if (bossesDefeated >= 4)")
rep("Game.cpp", "if (currentScore > 1000)", "if (bossesDefeated >= 5)")

rep("Game.cpp", "spawnEnemy(renderer);", """if (!bossActive && bossesDefeated < 5 && currentScore >= bossAt[bossesDefeated])
        {
            spawnEnemy(renderer);
            enemies.back()->scale = 2.5f;
            enemies.back()->hp = 5 + bossesDefeated * 2;
            bossActive = true;
        }
        else if (!bossActive)
        {
            spawnEnemy(renderer);
        }""")

print("JEFE APLICADO")
