using System;
using System.Collections.Generic;
using System.Windows.Forms;

namespace Blackjack
{
    public partial class Form1 : Form
    {
        private Deck deck;
        private Hand playerHand;
        private Hand dealerHand;
        private bool gameOver = false;

        public Form1()
        {
            InitializeComponent();
            NewGame();
        }

        private void NewGame()
        {
            deck = new Deck();
            deck.Shuffle();
            playerHand = new Hand();
            dealerHand = new Hand();
            gameOver = false;

            playerHand.AddCard(deck.Deal());
            playerHand.AddCard(deck.Deal());
            dealerHand.AddCard(deck.Deal());
            dealerHand.AddCard(deck.Deal());

            UpdateUI();
        }

        private void UpdateUI()
        {
            playerCardsLabel.Text = "Player: " + string.Join(", ", playerHand.Cards);
            playerScoreLabel.Text = $"Score: {playerHand.GetScore()}";

            if (gameOver)
            {
                dealerCardsLabel.Text = "Dealer: " + string.Join(", ", dealerHand.Cards);
                dealerScoreLabel.Text = $"Dealer Score: {dealerHand.GetScore()}";
            }
            else
            {
                dealerCardsLabel.Text = "Dealer: " + dealerHand.Cards[0] + ", [Hidden]";
                dealerScoreLabel.Text = $"Dealer Score: {dealerHand.Cards[0].GetValue()}";
            }
            resultLabel.Text = "";
        }

        private void hitButton_Click(object sender, EventArgs e)
        {
            playerHand.AddCard(deck.Deal());
            UpdateUI();

            if (playerHand.GetScore() > 21)
            {
                resultLabel.Text = "Player busts! Dealer wins.";
                gameOver = true;
                hitButton.Enabled = false;
                standButton.Enabled = false;
            }
        }

        private void standButton_Click(object sender, EventArgs e)
        {
            gameOver = true;
            while (dealerHand.GetScore() < 17)
            {
                dealerHand.AddCard(deck.Deal());
            }
            UpdateUI();
            CheckResult();
        }

        private void newGameButton_Click(object sender, EventArgs e)
        {
            NewGame();
            hitButton.Enabled = true;
            standButton.Enabled = true;
        }

        private void CheckResult()
        {
            int playerScore = playerHand.GetScore();
            int dealerScore = dealerHand.GetScore();

            if (playerScore > 21)
            {
                resultLabel.Text = "Player busts! Dealer wins.";
            }
            else if (dealerScore > 21)
            {
                resultLabel.Text = "Dealer busts! Player wins!";
            }
            else if (playerScore > dealerScore)
            {
                resultLabel.Text = "Player wins!";
            }
            else if (dealerScore > playerScore)
            {
                resultLabel.Text = "Dealer wins.";
            }
            else
            {
                resultLabel.Text = "Push (tie).";
            }
        }
    }

    public class Card
    {
        public string Suit { get; set; }
        public string Rank { get; set; }

        public Card(string suit, string rank)
        {
            Suit = suit;
            Rank = rank;
        }

        public int GetValue()
        {
            switch (Rank)
            {
                case "J":
                case "Q":
                case "K":
                    return 10;
                case "A":
                    return 11;
                default:
                    return int.Parse(Rank);
            }
        }

        public override string ToString()
        {
            return $"{Rank} of {Suit}";
        }
    }

    public class Deck
    {
        private List<Card> cards;
        private Random rng = new Random();

        public Deck()
        {
            cards = new List<Card>();
            string[] suits = { "♠", "♥", "♦", "♣" };
            string[] ranks = { "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A" };

            foreach (var suit in suits)
            {
                foreach (var rank in ranks)
                {
                    cards.Add(new Card(suit, rank));
                }
            }
        }

        public void Shuffle()
        {
            int n = cards.Count;
            while (n > 1)
            {
                n--;
                int k = rng.Next(n + 1);
                (cards[k], cards[n]) = (cards[n], cards[k]);
            }
        }

        public Card Deal()
        {
            if (cards.Count == 0)
                throw new InvalidOperationException("Deck is empty");
            Card card = cards[0];
            cards.RemoveAt(0);
            return card;
        }
    }

    public class Hand
    {
        public List<Card> Cards { get; private set; }

        public Hand()
        {
            Cards = new List<Card>();
        }

        public void AddCard(Card card)
        {
            Cards.Add(card);
        }

        public int GetScore()
        {
            int score = 0;
            int aces = 0;

            foreach (var card in Cards)
            {
                if (card.Rank == "A")
                {
                    aces++;
                    score += 11;
                }
                else
                {
                    score += card.GetValue();
                }
            }

            while (score > 21 && aces > 0)
            {
                score -= 10;
                aces--;
            }

            return score;
        }
    }
}