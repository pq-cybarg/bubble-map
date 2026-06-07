// Headless runner for Alloy commands (no GUI). Compile against the AlloyTools dist jar.
//   javac -cp org.alloytools.alloy.dist.jar RunAlloy.java
//   java  -cp org.alloytools.alloy.dist.jar:. RunAlloy BubbleStructure.als
import edu.mit.csail.sdg.alloy4.A4Reporter;
import edu.mit.csail.sdg.ast.Command;
import edu.mit.csail.sdg.parser.CompModule;
import edu.mit.csail.sdg.parser.CompUtil;
import edu.mit.csail.sdg.translator.A4Options;
import edu.mit.csail.sdg.translator.A4Solution;
import edu.mit.csail.sdg.translator.TranslateAlloyToKodkod;

public class RunAlloy {
  public static void main(String[] args) throws Exception {
    A4Reporter rep = new A4Reporter();
    CompModule world = CompUtil.parseEverything_fromFile(rep, null, args[0]);
    A4Options opt = new A4Options();   // default solver (SAT4J, pure-Java)
    System.out.println("=== Alloy check results for " + args[0] + " ===");
    for (Command c : world.getAllCommands()) {
      A4Solution sol = TranslateAlloyToKodkod.execute_command(rep, world.getAllReachableSigs(), c, opt);
      boolean sat = sol.satisfiable();
      String verdict;
      if (c.check) {
        // 'check' searches for a counterexample: SAT = assertion FAILS, UNSAT = assertion HOLDS
        verdict = sat ? "COUNTEREXAMPLE FOUND -> assertion FAILS" : "no counterexample -> assertion HOLDS";
      } else {
        verdict = sat ? "instance FOUND (satisfiable)" : "no instance (unsatisfiable)";
      }
      System.out.println(String.format("%-45s %s", c.label, verdict));
    }
  }
}
