open Google.OrTools.Sat
open System.IO
open System.Text.RegularExpressions

type button =
    { id: int
      affects_positions: int array }

type machine =
    { lights: int array
      buttons: button array
      expected_joltage: int array }

let parse_machine s =
    let lights =
        Regex.Match(s, @"\[(.+)\]").Groups[1].Value.ToCharArray()
        |> Array.map (fun c -> if c = '#' then 1 else 0)
    let buttons =
        Regex.Matches(s, @"\(([^()]+)\)")
        |> Seq.mapi (fun i m ->
            let x = m.Groups[1].Value.Split(',') |> Seq.map int |> Seq.toArray
            { id = i; affects_positions = x })
        |> Seq.toArray
    let expected_joltage =
        Regex.Match(s, @"\{([\d\,?]+)\}").Groups[1].Value.Split(",")
        |> Seq.map int
        |> Seq.toArray

    { lights = lights
      buttons = buttons
      expected_joltage = expected_joltage }

let solve_machine_for_lights machine =
    let model = new CpModel()
    let solver = new CpSolver()

    let buttons_pressed =
        Array.create machine.buttons.Length 0
        |> Array.map (fun i -> model.NewIntVar(0, 1, $"button_pressed_{i}") :> LinearExpr)

    machine.lights
    |> Array.iteri (fun i expected ->
        let toggled_buttons =
            machine.buttons
            |> Array.filter (fun b -> Array.contains i b.affects_positions)
            |> Array.map (fun b -> buttons_pressed[b.id])
        let total_toggles = model.NewIntVar(0, machine.buttons.Length, $"total_toggles_{i}")
        model.Add(LinearExpr.(=) (total_toggles, LinearExpr.Sum toggled_buttons))
        |> ignore
        model.AddModuloEquality(expected, total_toggles, 2) |> ignore
        ())

    model.Minimize(LinearExpr.Sum buttons_pressed)

    let status = solver.Solve model
    assert (status = CpSolverStatus.Optimal || status = CpSolverStatus.Feasible)

    buttons_pressed |> Array.map (fun b -> solver.Value(b)) |> Array.sum

let solve_machine_for_joltage machine =
    let model = new CpModel()
    let solver = new CpSolver()

    let buttons_pressed =
        Array.create machine.buttons.Length 0
        |> Array.map (fun i -> model.NewIntVar(0, 1000, $"button_pressed_{i}") :> LinearExpr)

    machine.expected_joltage
    |> Array.iteri (fun i expected ->
        let joltage_increments =
            machine.buttons
            |> Array.filter (fun b -> Array.contains i b.affects_positions)
            |> Array.map (fun b -> buttons_pressed[b.id])
        model.Add(LinearExpr.(=) (LinearExpr.Constant expected, LinearExpr.Sum joltage_increments))
        |> ignore)

    model.Minimize(LinearExpr.Sum buttons_pressed)

    let status = solver.Solve model
    assert (status = CpSolverStatus.Optimal || status = CpSolverStatus.Feasible)

    buttons_pressed |> Array.map (fun b -> solver.Value(b)) |> Array.sum

let solve machines solver = machines |> Seq.map solver |> Seq.sum

[<EntryPoint>]
let main argv =
    let fname = "example.txt"
    let machines = File.ReadLines fname |> Seq.map parse_machine

    printfn "Task 1: %i" (solve machines solve_machine_for_lights)
    printfn "Task 2: %i" (solve machines solve_machine_for_joltage)

    0
