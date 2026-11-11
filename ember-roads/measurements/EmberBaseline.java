import java.io.File;
import java.util.*;
import game.Game;
import other.GameLoader;
import other.context.Context;
import other.trial.Trial;
import other.move.Move;
import metrics.Metric;
import metrics.MetricsTracker;
import metrics.single.outcome.Balance;
import metrics.single.outcome.Completion;
import metrics.single.duration.DurationTurns;
import metrics.single.complexity.DecisionMoves;

public class EmberBaseline {
  public static void main(String[] args) throws Exception {
    if (args.length < 1)
      throw new IllegalArgumentException("Usage: EmberBaseline game.lud [trials] [seed]");

    int trials = args.length > 1 ? Integer.parseInt(args[1]) : 20;
    long seed = args.length > 2 ? Long.parseLong(args[2]) : 20261110L;

    Game game = GameLoader.loadGameFromFile(new File(args[0]));
    if (game == null) throw new IllegalStateException("Could not load game");

    List<Metric> metrics = Arrays.asList(
      new Balance(), new Completion(),
      new DurationTurns(), new DecisionMoves()
    );
    MetricsTracker tracker = new MetricsTracker(metrics);
    Random rng = new Random(seed);

    int finished = 0, capped = 0, totalMoves = 0;
    long legalSum = 0;
    int positions = 0;
    final int cap = 1000;

    for (int i = 0; i < trials; i++) {
      Trial trial = new Trial(game);
      Context context = new Context(game, trial);
      game.start(context);
      tracker.startNewTrial(context, trial);

      int moves = 0;
      while (!trial.over() && moves < cap) {
        int count = game.moves(context).count();
        if (count == 0)
          throw new IllegalStateException("No moves but trial not over");

        legalSum += count;
        positions++;

        Move move = game.moves(context).get(rng.nextInt(count));
        game.apply(context, move);
        moves++;
        tracker.observeNextState(context);
      }

      tracker.observeFinalState(context);
      if (trial.over()) finished++;
      else capped++;
      totalMoves += moves;
    }

    Map<String, Double> values = tracker.finaliseMetrics(game, trials);

    System.out.println("game=" + game.name());
    System.out.println("trials=" + trials + " seed=" + seed);
    System.out.println("max_moves_per_trial=" + cap);
    System.out.println("finished=" + finished + " capped=" + capped);
    System.out.println("mean_moves=" + ((double) totalMoves / trials));
    System.out.println("mean_legal_moves=" +
      (positions == 0 ? "n/a" : (double) legalSum / positions));

    for (Map.Entry<String, Double> e : values.entrySet())
      System.out.println(e.getKey() + "=" + e.getValue());
  }
}
