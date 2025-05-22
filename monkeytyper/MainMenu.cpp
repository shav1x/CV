#include "MainMenu.h"

MainMenu::MainMenu(float width, float height) {

    font.loadFromFile("../Fonts/varosta.ttf");

    mainMenu[0].setFont(font);
    mainMenu[0].setFillColor(sf::Color::White);
    mainMenu[0].setString("Play");
    mainMenu[0].setCharacterSize(150);
    mainMenu[0].setPosition(380, 230);

    mainMenu[1].setFont(font);
    mainMenu[1].setFillColor(sf::Color::White);
    mainMenu[1].setString("Options");
    mainMenu[1].setCharacterSize(70);
    mainMenu[1].setPosition(150, 400);

    mainMenu[2].setFont(font);
    mainMenu[2].setFillColor(sf::Color::White);
    mainMenu[2].setString("Exit");
    mainMenu[2].setCharacterSize(70);
    mainMenu[2].setPosition(150, 500);

    MainMenuSelected = 0;
    mainMenu[0].setFillColor(sf::Color::Green);
}

MainMenu::~MainMenu() = default;

void MainMenu::draw(sf::RenderWindow& window) {
    for (int i = 0; i < Max_main_menu; i++){
        window.draw(mainMenu[i]);
    }
}

void MainMenu::MoveUp() {
    if (MainMenuSelected + 1 >= 0){
        mainMenu[MainMenuSelected].setFillColor(sf::Color::White);
        MainMenuSelected--;
        if (MainMenuSelected == -1){
            MainMenuSelected = 2;
        }
        if (MainMenuSelected == 0)
            mainMenu[MainMenuSelected].setFillColor(sf::Color::Green);
        else
            mainMenu[MainMenuSelected].setFillColor(sf::Color::Blue);
    }
}

void MainMenu::MoveDown() {
    if (MainMenuSelected + 1 <= Max_main_menu) {
        mainMenu[MainMenuSelected].setFillColor(sf::Color::White);
        MainMenuSelected++;
        if (MainMenuSelected == 3){
            MainMenuSelected = 0;
        }
        if (MainMenuSelected == 0)
            mainMenu[MainMenuSelected].setFillColor(sf::Color::Green);
        else
            mainMenu[MainMenuSelected].setFillColor(sf::Color::Blue);
    }
}
