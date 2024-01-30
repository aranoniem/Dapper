# RailNL Dapper
### Overview
Dapper RailNL is a project for the minor Programming at the University of Amsterdam. The project aims to provide a solution for the most optimal rail network in the Netherlands. To create  these solutions multiple types of algorithms are performed on a dataset that contains all stations, all their connections and the distance between these stations in minutes. With the found optimal solution a visualization is constructed based on a dataset that contains the coordinates of all stations. The purpose of this is to search for the best solution possible but also to research the differences in constructive and iterative algorithms. 

## Get started
### Prerequisites
This code is written using Python 3.6 and up. To get started, it is important to clone this directory onto your own computer. After downloading, go to the directory.


> git clone https://github.com/aranoniem/Dapper.git
>
> cd Dapper


In requirements.txt are packages needed to run this directory smoothly. These are easily installed via pip, using the following command:

> pip install - r requirements.txt

### Usage
The program can be used with two datasets: Holland and Nationaal. You could use either by calling it in the place of “dataset”, or when using Holland to leave “dataset” empty.

> python3 main.py “dataset”

This will prompt you for an algorithm with which you would like create a rail network, how many trajectories can be used as a maximum and how long each trajectory may be timewise. The program will output the generated rail network and its quality score (K).

### Structure 
The following list describes the organization of the directory and its most important components.
* **/code**: contains all the code of this project
    * **/algorithms**: contains all the algorithms available for creating a railnetwork
    * **/classes**: contains 4 classes; 3 to store data and 1 load data into memory
    * **/visualisation**: contains files for visual images of the railnetwork
* **/data**: contains datafiles of stations and connections. Two files per area.
* **/images**: contains images of railnetwork visualisation and output
* **/plots**: contains histograms of experiments with algorithms
* **/result_csv**: contains data from experimenting with algorithms
* **/shapefile_for_visualisation**: contains files necessary to load the map of the created rail network

## Algorithms
We have created multiple algorithms to use in the project. To give an overview:
* BreadthFirst
* DepthFirst
* Greedy
* Two Local Searches
* Two Random algorithms
The algorithms will be shortly explained in the paragraphs below.

### BreadthFirst
BreadthFirst is implemented using a parentclass of DepthFirst. It creates a tree with a random starting station and creates connections based on the layers of the tree. It creates a railnetwork by comparing the qualityscore between single and multiple trajectories taken from said tree.

### DepthFirst
DepthFirst creates a tree from a random starting station. It searches for all the connections to the starting station with a depth of the maximum time a trajectory may take. Once this depth is reached, a rail network is created by comparing the qualityscore between single and multiple trajectories taken from said tree.

### Greedy

### Local Search 1

### Local Search 2

### Semi-Random

### Totally-Random

## Visualization (todo: plaatjes maken van up to date staat en toevoegen)
### map visualisation
![Map visualisation](/images/Map%20of%20railNL%20v1.jpg)

### our current output
![Current output](/images/RailNL%20output%2012%201%202024.png)
## Authors
* Paco van der Vliet
* David Verboom
* Anouk Raanhuis
