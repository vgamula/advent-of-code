open Google.OrTools.Sat
open System.IO
open System.Text.RegularExpressions

type Button =
    { id: int
      affects_positions: int array }

type Machine =
    { Lights: int array
      Buttons: Button array
      Joltage: int array }

let ParseMachine s =
    let lights =
        Regex.Match(s, @"\[(.+)\]").Groups[1].Value.ToCharArray()
        |> Array.map (fun c -> if c = '#' then 1 else 0)
    let buttons =
        Regex.Matches(s, @"\(([^()]+)\)")
        |> Seq.mapi (fun i m ->
            let x = m.Groups[1].Value.Split(',') |> Seq.map int |> Seq.toArray
            { id = i; affects_positions = x })
        |> Seq.toArray
    let joltage =
        Regex.Match(s, @"\{([\d\,?]+)\}").Groups[1].Value.Split(",")
        |> Seq.map int
        |> Seq.toArray

    { Lights = lights
      Buttons = buttons
      Joltage = joltage }

let SolveMachineForLights machine =
    let model = new CpModel()
    let solver = new CpSolver()

    let buttons_pressed =
        Array.init machine.Buttons.Length (fun i -> model.NewIntVar(0, 1, $"button_pressed_{i}") :> LinearExpr)

    machine.Lights
    |> Array.iteri (fun i expected ->
        let toggled_buttons =
            machine.Buttons
            |> Array.filter (fun b -> Array.contains i b.affects_positions)
            |> Array.map (fun b -> buttons_pressed[b.id])
        let total_toggles = model.NewIntVar(0, machine.Buttons.Length, $"total_toggles_{i}")
        model.Add(LinearExpr.(=) (total_toggles, LinearExpr.Sum toggled_buttons))
        |> ignore
        model.AddModuloEquality(expected, total_toggles, 2) |> ignore)

    model.Minimize(LinearExpr.Sum buttons_pressed)

    let status = solver.Solve model
    assert (status = CpSolverStatus.Optimal || status = CpSolverStatus.Feasible)

    buttons_pressed |> Array.map (fun b -> solver.Value(b)) |> Array.sum

let SolveMachineForJoltage machine =
    let model = new CpModel()
    let solver = new CpSolver()

    let buttons_pressed =
        Array.init machine.Buttons.Length (fun i -> model.NewIntVar(0, 1000, $"button_pressed_{i}") :> LinearExpr)

    machine.Joltage
    |> Array.iteri (fun i expected ->
        let joltage_increments =
            machine.Buttons
            |> Array.filter (fun b -> Array.contains i b.affects_positions)
            |> Array.map (fun b -> buttons_pressed[b.id])
        model.Add(LinearExpr.(=) (LinearExpr.Constant expected, LinearExpr.Sum joltage_increments))
        |> ignore)

    model.Minimize(LinearExpr.Sum buttons_pressed)

    let status = solver.Solve model
    assert (status = CpSolverStatus.Optimal || status = CpSolverStatus.Feasible)

    buttons_pressed |> Array.map (fun b -> solver.Value(b)) |> Array.sum

[<EntryPoint>]
let main argv =
    let fname = "example.txt"
    let machines = File.ReadLines fname |> Seq.map ParseMachine

    printfn "Task 1: %i" (Seq.sumBy SolveMachineForLights machines)
    printfn "Task 2: %i" (Seq.sumBy SolveMachineForJoltage machines)

    0
