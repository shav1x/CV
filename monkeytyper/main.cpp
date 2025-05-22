#include <iostream>
#include <fmt/ranges.h>
#include <SFML/Graphics.hpp>
#include "MainMenu.h"
#include "Game.h"
#include "Options.h"


auto main() -> int {

    sf::RenderWindow menu(sf::VideoMode(1920, 1080), "Main Menu", sf::Style::Default);
    MainMenu mainMenu(menu.getSize().x, menu.getSize().y);

    sf::RectangleShape mainMenuBackground;
    mainMenuBackground.setSize(sf::Vector2f(1920, 1080));
    sf::Texture mainMenuTexture;
    mainMenuTexture.loadFromFile("../Images/monkey.jpg");
    mainMenuBackground.setTexture(&mainMenuTexture);

    Options options;


    while (menu.isOpen()) {
        sf::Event ev;
        while (menu.pollEvent(ev)) {

            if (ev.type == sf::Event::Closed) {
                menu.close();
            }

            if (ev.type == sf::Event::KeyPressed) {

                if (ev.key.code == sf::Keyboard::Up) {
                    mainMenu.MoveUp();
                    break;
                }

                if (ev.key.code == sf::Keyboard::Down) {
                    mainMenu.MoveDown();
                    break;
                }

                if (ev.key.code == sf::Keyboard::Return) {

                    int x = mainMenu.MainMenuPressed();

                    if (x == 0) {

                        sf::RenderWindow monkeytypeWin(sf::VideoMode(1920, 1080), "Monkey Type", sf::Style::Default);
                        Game monkeytype;

                        sf::RectangleShape monkeytypeBackground;
                        monkeytypeBackground.setSize(sf::Vector2f(1920, 1080));
                        sf::Texture monkeytypeTexture;
                        monkeytypeTexture.loadFromFile("../Images/stars.jpeg");
                        monkeytypeBackground.setTexture(&monkeytypeTexture);

                        sf::RectangleShape rect(sf::Vector2f(1920, 250));
                        rect.setFillColor(sf::Color::Black);
                        rect.setPosition(0, 660);
                        rect.setOutlineThickness(20);
                        rect.setOutlineColor(sf::Color(255, 165, 0));

                        sf::Clock clock;

                        while (monkeytypeWin.isOpen()) {

                            sf::Event playEv;

                            while (monkeytypeWin.pollEvent(playEv)) {

                                if (playEv.type == sf::Event::Closed) {
                                    monkeytypeWin.close();
                                }

                                if (playEv.type == sf::Event::KeyPressed) {
                                    if (playEv.key.code == sf::Keyboard::Escape) {
                                        monkeytypeWin.close();
                                    }
                                    if (playEv.key.code == sf::Keyboard::Return) {
                                        // Find the value in wordsText
                                        auto it = std::find(monkeytype.textDisplayed.begin(),
                                                            monkeytype.textDisplayed.end(),
                                                            monkeytype.input.getString());
                                        if (it != monkeytype.textDisplayed.end()) {
                                            // Remove the value from wordsText
                                            auto iter = monkeytype.wordsText.begin();
                                            for (int i = 0; i < monkeytype.wordsText.size(); i++) {
                                                if (monkeytype.wordsText[i].getString() == *it) {
                                                    monkeytype.wordsText.erase(iter);
                                                    monkeytype.score++;
                                                    monkeytype.scoreText.setString(std::to_string(monkeytype.score));
                                                }
                                                else iter++;
                                            }
                                            monkeytype.textDisplayed.erase(it);
                                        }
                                        // Clear the input
                                        monkeytype.input.setString("");
                                    }
                                }

                                if (playEv.type == sf::Event::TextEntered) {
                                    if (playEv.text.unicode < 128 && playEv.text.unicode != 13) {
                                        if (playEv.text.unicode == 8) {  // If backspace is pressed
                                            std::string temp = monkeytype.input.getString();
                                            temp = temp.substr(0, temp.length() - 1);  // Remove the last character
                                            monkeytype.input.setString(temp);  // Set the new string
                                        } else if (playEv.text.unicode >= 32 && playEv.text.unicode < 128) {
                                            monkeytype.input.setString(monkeytype.input.getString() + static_cast<char>(playEv.text.unicode));
                                        }
                                    }
                                }

                            }

                            monkeytype.update(clock, options);
                            monkeytypeWin.clear();
                            monkeytypeWin.draw(monkeytypeBackground);
                            monkeytypeWin.draw(rect);
                            monkeytype.draw(monkeytypeWin);
                            monkeytypeWin.display();

                        }

                    }

                    if (x == 1) {

                        sf::RenderWindow optionsWindow(sf::VideoMode(960, 720), "Options", sf::Style::Default);

                        while (optionsWindow.isOpen()) {
                            sf::Event opEvent;
                            while (optionsWindow.pollEvent(opEvent)) {
                                if (opEvent.type == sf::Event::Closed) {
                                    optionsWindow.close();
                                }
                                if (opEvent.type == sf::Event::KeyPressed) {
                                    if (opEvent.key.code == sf::Keyboard::Escape) {
                                        optionsWindow.close();
                                    }
                                    if (opEvent.key.code == sf::Keyboard::Up) {
                                        options.MoveUp();
                                        break;
                                    }
                                    if (opEvent.key.code == sf::Keyboard::Down) {
                                        options.MoveDown();
                                        break;
                                    }
                                    if (opEvent.key.code == sf::Keyboard::Return) {
                                        options.numOfLetters = options.optionsPressed();
                                        optionsWindow.close();
                                    }
                                }
                            }
                            optionsWindow.clear();
                            options.draw(optionsWindow);
                            optionsWindow.display();
                        }
                    }

                    if (x == 2) {
                        menu.close();
                    }

                    break;

                }
            }
        }

        menu.clear();
        menu.draw(mainMenuBackground);
        mainMenu.draw(menu);
        menu.display();

    }

}
