#include "Options.h"

Options::Options() {

    optionsFont.loadFromFile("../Fonts/varosta.ttf");
    text.setFont(optionsFont);
    text.setString("The number of letters in each word: ");
    text.setCharacterSize(60);
    text.setPosition(30, 150);

    numOfLetters = 0;

    letters[0].setFont(optionsFont);
    letters[0].setFillColor(sf::Color::White);
    letters[0].setString("Any (default)");
    letters[0].setCharacterSize(50);
    letters[0].setPosition(100, 250);

    letters[1].setFont(optionsFont);
    letters[1].setFillColor(sf::Color::White);
    letters[1].setString("Length of each word is 5");
    letters[1].setCharacterSize(50);
    letters[1].setPosition(100, 320);

    letters[2].setFont(optionsFont);
    letters[2].setFillColor(sf::Color::White);
    letters[2].setString("Length of each word is 6");
    letters[2].setCharacterSize(50);
    letters[2].setPosition(100, 390);

    letters[3].setFont(optionsFont);
    letters[3].setFillColor(sf::Color::White);
    letters[3].setString("Length of each word is 7");
    letters[3].setCharacterSize(50);
    letters[3].setPosition(100, 460);

    optionsSelected = 0;
    letters[0].setFillColor(sf::Color::Red);
};

Options::~Options() = default;

void Options::MoveDown() {
    if (optionsSelected + 1 <= 4) {
        letters[optionsSelected].setFillColor(sf::Color::White);
        optionsSelected++;
        if (optionsSelected == 4) {
            optionsSelected = 0;
        }
        letters[optionsSelected].setFillColor(sf::Color::Red);
    }
    if (optionsSelected == 0)
        numOfLetters = 0;
    else numOfLetters = optionsSelected + 4;
}

void Options::MoveUp() {
    if (optionsSelected + 1 >= 0) {
        letters[optionsSelected].setFillColor(sf::Color::White);
        optionsSelected--;
        if (optionsSelected == -1) {
            optionsSelected = 3;
        }
        letters[optionsSelected].setFillColor(sf::Color::Red);
    }
    if (optionsSelected == 0)
        numOfLetters = 0;
    else numOfLetters = optionsSelected + 4;
}

void Options::draw(sf::RenderWindow& window) {
    window.draw(text);
    for (int i = 0; i < 4; i++)
        window.draw(letters[i]);
}
