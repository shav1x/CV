#pragma once
#include <SFML/Graphics.hpp>
#include <iostream>
#include <queue>
#include <set>
#include "Options.h"

class Game {

public:
    Game();

    void draw(sf::RenderWindow& window);

    void drawWin(sf::RenderWindow& window);

    void update(sf::Clock& clock, Options opt);

    ~Game();



private:
    sf::Font wordsFont;
    sf::Font otherFont;
    sf::RectangleShape rect;
    std::vector<bool> processed;
    int currentIndex;
    float speed;
    int health;

public:
    std::vector<std::string> words1;
    std::vector<sf::Text> wordsText;
    std::vector<std::string> textDisplayed;
    int score;
    sf::Text input;
    sf::Text speedText;
    sf::Text healthText;
    sf::Text scoreText;
    sf::Text h;
    sf::Text s;

};
