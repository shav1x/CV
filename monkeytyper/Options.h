#pragma once
#include <SFML/Graphics.hpp>

class Options {

public:

    Options();

    int numOfLetters;

    sf::Text letters[4];

    void draw(sf::RenderWindow &window);

    int optionsPressed() {
        return optionsSelected > 0 ? optionsSelected + 4 : 0;
    }

    void MoveUp();

    void MoveDown();

    ~Options();

    int optionsSelected;

private:
    sf::Font optionsFont;
    sf::Text text;
};

