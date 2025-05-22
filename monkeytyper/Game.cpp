#include "Game.h"
#include "Options.h"
#include <SFML/Graphics.hpp>
#include <fstream>
#include <random>

Game::Game() {

    currentIndex = 0;


    score = 0;

    health = 3;

    speed = 60.0f;

    wordsFont.loadFromFile("../Fonts/SweetCharmy.ttf");
    otherFont.loadFromFile("../Fonts/varosta.ttf");

    speedText.setFont(otherFont);
    speedText.setString(std::to_string(speed));
    speedText.setPosition(165, 780);
    speedText.setCharacterSize(30);
    speedText.setFillColor(sf::Color::White);

    h.setString("Health: ");
    h.setFont(otherFont);
    h.setCharacterSize(60);
    h.setPosition(1150, 690);
    h.setFillColor(sf::Color::Red);

    healthText.setFont(otherFont);
    healthText.setString(std::to_string(health));
    healthText.setPosition(1340, 690);
    healthText.setCharacterSize(60);
    healthText.setFillColor(sf::Color::Red);

    s.setString("Score: ");
    s.setFont(otherFont);
    s.setCharacterSize(60);
    s.setPosition(130, 690);
    s.setFillColor(sf::Color(255, 165, 0));

    scoreText.setFont(otherFont);
    scoreText.setString(std::to_string(score));
    scoreText.setPosition(300, 690);
    scoreText.setCharacterSize(60);
    scoreText.setFillColor(sf::Color(255, 165, 0));

    rect.setSize(sf::Vector2f(500, 50));
    rect.setFillColor(sf::Color::White);
    rect.setPosition(500, 700);

    input.setFont(otherFont);
    input.setString("");
    input.setCharacterSize(40);
    input.setFillColor(sf::Color::Black);
    input.setPosition(505, 705);

    std::ifstream file("../Words1.txt");

    std::string word;

    while (file >> word) {
        words1.push_back(word);
    }

    std::random_device rd;

    std::mt19937 g(rd());

    std::shuffle(words1.begin(), words1.end(), g);

    for (int i = 0; i < words1.size(); i++) {
        sf::Text txt;
        txt.setFillColor(sf::Color::White);
        txt.setFont(wordsFont);
        txt.setCharacterSize(40);
        txt.setString(words1[i]);

        txt.setPosition(-240, 50 + std::rand() % 541);

        wordsText.push_back(txt);
    }

}

void Game::draw(sf::RenderWindow &window) {
    for (int i = 0; i <= currentIndex; i++)
        window.draw(wordsText[i]);
    window.draw(rect);
    window.draw(input);
    window.draw(speedText);
    window.draw(healthText);
    window.draw(scoreText);
    window.draw(h);
    window.draw(s);
}

void Game::drawWin(sf::RenderWindow &window) {
    sf::Text text;
    text.setCharacterSize(200);
    text.setString("You Win!");
    text.setFont(wordsFont);
    text.setPosition(400, 400);
    text.setFillColor(sf::Color(255, 165, 0));
    window.draw(text);
}

void Game::update(sf::Clock &clock, Options opt) {

    if(health != 0) {

        while (processed.size() < wordsText.size()) {
            processed.push_back(false);
        }
        sf::Time elapsed = clock.restart();
        speed += 0.0002f;
        speedText.setString(std::to_string(speed));
        for (int i = 0; i <= currentIndex && i < wordsText.size(); ++i) {
            sf::Text &currentText = wordsText[i];
            if (opt.numOfLetters != 0 && currentText.getString().getSize() != opt.numOfLetters) {
                if (i == currentIndex) {
                    ++currentIndex;
                }
                continue;
            }
            float newX = currentText.getPosition().x + speed * elapsed.asSeconds();
            currentText.setPosition(newX, currentText.getPosition().y);
            if (currentText.getPosition().x >= 940 && currentText.getPosition().x < 1200) {
                currentText.setFillColor(sf::Color::Yellow);
            } else if (currentText.getPosition().x >= 1200) {
                currentText.setFillColor(sf::Color::Red);
            }
            if (newX > 1513 && !processed[i]) {
                health--;
                healthText.setString(std::to_string(health));
                processed[i] = true;
            }
            if (i == currentIndex && newX >= 5.0f) {
                currentIndex++;
            }
            if (opt.numOfLetters == 0 || currentText.getString().getSize() == opt.numOfLetters) {
                textDisplayed.push_back(currentText.getString());
            }
        }
    }
    else return;

}

Game::~Game() = default;