defmodule Hellojoe do
  defmodule DialogueArgs do
    use TypedStruct

    typedstruct do
      field :from_name, String.t, enforce: true
      field :to_name, String.t, enforce: true
      field :secret, String.t, enforce: true
    end
  end

  defmodule MessageOp do
    use TypedStruct

    typedstruct do
      field :id, integer, enforce: true
      field :from, String.t, enforce: true
      field :to, String.t, enforce: true
      field :message, String.t, enforce: true
    end
  end

  defmodule GeneratedSequence do
    use TypedStruct

    typedstruct do
      field :ids, MapSet.t(integer), default: MapSet.new
      field :messages, [MessageOp.t], default: []
      field :rstate, :rand.state, enforce: true
      field :first_actor, String.t, enforce: true
    end
  end

  defmodule ServerCase do
    use TypedStruct

    typedstruct do
      field :recv_id, integer, enforce: true
      field :send_id, integer, enforce: true
      field :next_recv_id, integer, enforce: true
      field :recv_from, String.t, enforce: true
      field :send_to, String.t, enforce: true
      field :recv_message, String.t, enforce: true
      field :send_message, String.t, enforce: true
    end
  end

  defmodule ServerInfo do
    use TypedStruct

    typedstruct do
      field :name, String.t, enforce: true
      field :first_id, integer, enforce: true
      field :cases, [ServerCase.t], default: []
      field :first_message, MessageOp.t
    end
  end

  def names, do: [
    "Mike",
    "Joe",
    "Robert",
    "Theresa",
    "Jose",
    "Bogumil",
    "Björn",
    "Claes",
    "Tony",
    "Patrik",
    "Rickard",
    "Raimo",
    "Arndt",
  ]

  def to_bare_name(name), do: name |> String.downcase |> String.normalize(:nfd) |> String.replace(~r/[^A-z\s]/u, "") |> String.to_atom
  def to_server_name(name), do: String.to_atom("actor_#{to_bare_name(name)}_srv")
  def to_node_name(name), do: String.to_atom("actor@#{to_bare_name(name)}")
  def to_app_name(name), do: String.to_atom("actor_#{to_bare_name(name)}")
  def to_sup_name(name), do: String.to_atom("actor_#{to_bare_name(name)}_sup")

  def dialogues, do:
    [
      fn args -> [
        "Hello #{args.to_name}.",
        "Hello #{args.from_name}.",
        "System working?",
        "Seems to be.",
        "Okay, fine. The next sequence is #{args.secret}.",
      ] end,

      fn args -> [
        "Hello #{args.to_name}.",
        "Hello #{args.from_name}.",
        "I see you've managed to fix the bug then.",
        "Yes, finally.",
        "Okay. The sequence is #{args.secret}.",
      ] end,
    ]

  def final_message(actor), do: "Hello #{actor}."

  defp random_item(list, rstate) do
    {i, rstate} = :rand.uniform_s(Enum.count(list), rstate)
    item = Enum.fetch!(list, i - 1)
    {item, rstate}
  end

  defp generate_dialogue(seq = %GeneratedSequence{first_actor: first_actor}, [], _actors, actor) when first_actor == actor, do:
    %{
      seq |
      messages: Enum.reverse(seq.messages),
    }

  defp generate_dialogue(seq, [], actors, actor) do
    {id, ids, rstate} = next_id(seq.ids, seq.rstate)
    message = %MessageOp{
      id: id,
      from: actor,
      to: seq.first_actor,
      message: final_message(seq.first_actor),
    }
    seq = %{
      seq |
      messages: [message | seq.messages],
      ids: ids,
      rstate: rstate,
    }
    generate_dialogue(seq, [], actors, seq.first_actor)
  end

  defp generate_dialogue(seq, [secret | secrets], actors, actor) do
    other_actors = Enum.filter(actors, fn x -> x != actor end)
    {next_actor, rstate} = random_item(other_actors, seq.rstate)
    {dialogue_fn, rstate} = random_item(dialogues(), rstate)
    dialogue = dialogue_fn.(%DialogueArgs{
      from_name: actor,
      to_name: next_actor,
      secret: secret,
    })
    seq = %{
      seq |
      rstate: rstate,
    }
    generate_phrase(seq, secrets, actors, actor, next_actor, dialogue)
  end

  def next_id(ids, rstate) do
    {id, rstate} = :rand.uniform_s(1_000_000_000, rstate)
    if MapSet.member?(ids, id) do
      next_id(ids, rstate)
    else
      ids = MapSet.put(ids, id)
      {id, ids, rstate}
    end
  end

  defp generate_phrase(seq, secrets, actors, actor, _next_actor, []), do:
    generate_dialogue(seq, secrets, actors, actor)

  defp generate_phrase(seq, secrets, actors, actor, next_actor, [phrase | dialogue]) do
    {id, ids, rstate} = next_id(seq.ids, seq.rstate)
    message = %MessageOp{
      id: id,
      from: actor,
      to: next_actor,
      message: phrase,
    }
    seq = %{
      seq |
      rstate: rstate,
      messages: [message | seq.messages],
      ids: ids,
    }
    generate_phrase(seq, secrets, actors, next_actor, actor, dialogue)
  end

  def generate_sequence(actors, secrets, seed \\ nil) do
      rstate =
        case seed do
          nil -> :rand.seed_s(:exsss)
          seed -> :rand.seed_s(seed)
        end
      {first_actor, rstate} = random_item(actors, rstate)
      seq = %GeneratedSequence{
        rstate: rstate,
        first_actor: first_actor,
      }
      generate_dialogue(seq, secrets, actors, first_actor)
  end

  def get_actors(sequence) do
    froms = Enum.map(sequence.messages, fn msg -> msg.from end)
    tos = Enum.map(sequence.messages, fn msg -> msg.to end)
    Enum.concat(froms, tos) |> Enum.uniq
  end

  def generate_server_info(sequence, actor) do
    rot_messages = Enum.drop(sequence.messages, 1) ++ Enum.take(sequence.messages, 1)
    pairs =
      Enum.zip(sequence.messages, rot_messages)
      |> Enum.filter(fn {%MessageOp{to: to_actor}, _send_msg} -> to_actor == actor end)
    [{%MessageOp{id: first_id}, _} | _] = pairs
    cycled_pairs = Enum.map(Enum.drop(pairs, 1) ++ Enum.take(pairs, 1), fn {recv_msg, _send_msg} -> recv_msg end)
    cases =
      Enum.zip(pairs, cycled_pairs)
      |> Enum.map(fn {{recv_msg, send_msg}, next_recv_msg} -> %ServerCase{
           recv_message: recv_msg.message,
           send_message: send_msg.message,
           recv_id: recv_msg.id,
           next_recv_id: next_recv_msg.id,
           send_id: send_msg.id,
           recv_from: recv_msg.from,
           send_to: send_msg.to,
         } end)
    %ServerInfo{
      name: actor,
      cases: cases,
      first_id: first_id,
    }
  end

  def string_to_msg(msg) do
    msg
  end

  def generate_server_handler(case_info, name, opts) do
    log_messages = Keyword.get(opts, :log_messages)
    delay = 100 + :rand.uniform(200)
    quote do
      def handle_message(unquote(to_bare_name(case_info.recv_from)), unquote(string_to_msg(case_info.recv_message)), state = %{state: unquote(case_info.recv_id)}) do
        unquote_splicing(
          if !log_messages do
            []
          else
            [quote do
              :logger.notice(unquote('Received message from #{case_info.recv_from} to #{name}, id #{case_info.recv_id}: #{case_info.recv_message}'))
            end]
          end
        )
        receive do
          after unquote(delay) -> {}
        end
        {:ok, state} = send_message(
          state,
          unquote(to_bare_name(case_info.send_to)),
          unquote(string_to_msg(case_info.send_message))
        )
        state = %{state | state: unquote(case_info.next_recv_id)}
        {:noreply, state}
      end
    end
  end

  def cipher, do: :aes_256_ctr

  def generate_server(actors, name, opts \\ []) do
    remote_nodes = Keyword.get(opts, :remote_nodes)
    log_messages = Keyword.get(opts, :log_messages)
    actor_info = actors[name]
    other_actors = for {actor, _info} <- actors, actor != name, do: actor
    %{key_length: aes_key_length, iv_length: aes_iv_length} = :crypto.cipher_info(cipher())
    contents = quote location: :keep do
      @behaviour :gen_server

      defp send_message(state = %{rand_state: rand_state, key: key}, to_actor, message) do
        {iv, rand_state} = :rand.bytes_s(unquote(aes_iv_length), rand_state)
        encrypted = :crypto.crypto_one_time(unquote(cipher()), key, iv, message, [])

        :gen_server.cast(
          {:global, to_actor},
          {:message, unquote(to_bare_name(name)), iv, encrypted}
        )

        state = %{state | rand_state: rand_state}
        {:ok, state}
      end

      defp next_key_sync(state = %{remaining_key_syncs: 1}) do
        :logger.notice(unquote('#{name} joined the conference! Messages output is restricted.'))
        unquote_splicing(
          if !actor_info.first_message do
            []
          else
            [quote do
              {:ok, state} = send_message(state, unquote(to_bare_name(actor_info.first_message.to)), unquote(string_to_msg(actor_info.first_message.message)))
            end]
          end
        )
        state = %{state | remaining_key_syncs: 0}
        {:noreply, state}
      end

      defp next_key_sync(state = %{remaining_key_syncs: remaining_key_syncs}) do
        state = %{state | remaining_key_syncs: remaining_key_syncs - 1}
        {:noreply, state}
      end

      unquote_splicing(Enum.map(actor_info.cases, &generate_server_handler(&1, name, log_messages: log_messages)))

      def start_link() do
        :gen_server.start_link({:global, unquote(to_bare_name(name))}, __MODULE__, nil, [])
      end

      unquote(
        if remote_nodes do
          quote do
            defp do_await_other(retries, actor, _node, max_retries) when retries >= max_retries do
              throw ('Can\'t reach ' ++ :erlang.atom_to_list(actor))
            end

            defp do_await_other(retries, actor, node, max_retries) do
              case :global.whereis_name(actor) do
                pid when is_pid(pid) ->
                  :erlang.link(pid)
                  {:ok, pid}
                :undefined ->
                  receive do
                    after 1000 + 2000 * retries -> {}
                  end
                  case :net_adm.ping(node) do
                    :pong -> :global.sync()
                    :pang -> {}
                  end
                  do_await_other(retries + 1, actor, node, max_retries)
              end
            end

            defp await_other(actor, node, max_retries \\ 3) do
              do_await_other(0, actor, node, max_retries)
            end
          end
        else
          quote do
            defp do_await_other(retries, actor, max_retries) when retries >= max_retries do
              throw ('Can\'t reach ' ++ :erlang.atom_to_list(actor))
            end

            defp do_await_other(retries, actor, max_retries) do
              case :global.whereis_name(actor) do
                pid when is_pid(pid) -> {:ok, pid}
                :undefined ->
                  receive do
                    after 1000 + 2000 * retries -> {}
                  end
                  do_await_other(retries + 1, actor, max_retries)
              end
            end

            defp await_other(actor, max_retries \\ 3) do
              do_await_other(0, actor, max_retries)
            end
          end
        end
      )

      @impl true
      def init(_args) do
        unquote_splicing(
          for other_name <- other_actors do
            if remote_nodes do
              quote do
                await_other(unquote(to_bare_name(other_name)), unquote(to_node_name(other_name)))
              end
            else
              quote do
                await_other(unquote(to_bare_name(other_name)))
              end
            end
          end
        )

        rand_state = :crypto.rand_seed_s()
        {key, rand_state} = :rand.bytes_s(unquote(aes_key_length), rand_state)
        unquote_splicing(
          for other_name <- other_actors do
            quote do
              :gen_server.cast({:global, unquote(to_bare_name(other_name))}, {:key, key})
            end
          end
        )

        state = %{
          state: unquote(actor_info.first_id),
          remaining_key_syncs: unquote(length(other_actors)),
          key: key,
          rand_state: rand_state,
        }
        {:ok, state}
      end

      @impl true
      def handle_call(_message, _from, _state) do
        throw 'Unexpected call'
      end

      @impl true
      def handle_cast({:key, other_key}, state = %{key: key}) do
        new_key = :crypto.exor(other_key, key)
        state = %{state | key: new_key}
        next_key_sync(state)
      end

      @impl true
      def handle_cast({:message, from, iv, encrypted}, state = %{key: key}) do
        message = :crypto.crypto_one_time(unquote(cipher()), key, iv, encrypted, [])
        handle_message(from, message, state)
      end
    end

    {to_server_name(name), contents}
  end

  def generate_app(name) do
    contents = quote location: :keep do
      @behaviour :application

      @impl true
      def start(_type, _args) do
        unquote(to_sup_name(name)).start_link()
      end

      @impl true
      def stop(_state) do
        :ok
      end
    end

    {to_app_name(name), contents}
  end

  def generate_supervisor(name) do
    contents = quote location: :keep do
      @behaviour :supervisor

      def start_link() do
        :supervisor.start_link(__MODULE__, [])
      end

      @impl true
      def init(_args) do
        sup_flags = %{}
        children = [
          %{
            id: unquote(to_server_name(name)),
            start: {unquote(to_server_name(name)), :start_link, []},
          }
        ]
        {:ok, {sup_flags, children}}
      end
    end
    {to_sup_name(name), contents}
  end

  defp write_config(contents, path) do
    File.write!(path, :io_lib.format("~p.~n", [contents]))
  end

  @extra_chunks MapSet.new(['Attr', 'Line', 'Type'])
  defp full_strip(beam) do
    {:ok, {_mod, beam}} = :beam_lib.strip(beam)
    {:ok, _, chunks} = :beam_lib.all_chunks(beam)
    chunks = Enum.filter(chunks, fn {name, _chunk} -> not MapSet.member?(@extra_chunks, name) end)
    :beam_lib.build_module(chunks)
  end

  def write_single_app(server_infos, name, path, opts \\ []) do
    log_messages = Keyword.get(opts, :log_messages)
    mods = [
      generate_server(server_infos, name, remote_nodes: true, log_messages: log_messages),
      generate_app(name),
      generate_supervisor(name),
    ]
    for {name, contents} <- mods do
      {:module, _mod, beam, _term} = Module.create(name, contents, Macro.Env.location(__ENV__))
      {:ok, beam} = full_strip(beam)
      File.write!(Path.join(path, "#{name}.beam"), beam, [:binary])
    end

    app_spec = {
      :application, to_app_name(name), [
        applications: [:kernel, :stdlib, :crypto],
        mod: {to_app_name(name), []},
      ]
    }
    write_config(app_spec, Path.join(path, "#{to_app_name(name)}.app"))

    :ok
  end

  def generate_dockerfile(name, path) do
    sys_config = [
      kernel: [
        logger: [
          {:handler, :default, :logger_std_h, %{
              formatter: {:logger_formatter, %{}},
           }},
        ],
      ]
    ]
    write_config(sys_config, Path.join(path, "sys.config"))

    contents = """
    FROM erlang:26-alpine
    ENV LANG=C.UTF-8
    COPY sys.config /root/sys.config
    COPY ebin /root/ebin
    CMD [ \
      "erl", \
      "-config", "/root/sys.config", \
      "-pa", "/root/ebin", \
      "-sname", "actor", \
      "-setcookie", "cookie", \
      "-noshell", \
      "-eval", "{ok, _Started} = application:ensure_all_started(#{to_app_name(name)}, permanent)" \
    ]
    """
    File.write!(Path.join(path, "Dockerfile"), contents)
  end

  def generate_compose(actors, path) do
    services =
      for {name, _actor_info} <- actors, into: %{} do
        service =
          %{
            build: "./#{to_bare_name(name)}",
            hostname: to_bare_name(name),
          }
        {to_bare_name(name), service}
      end
    contents = %{
      services: services,
    }
    compose_path = Path.join(path, "docker-compose.yml")
    File.write!(compose_path, Jason.encode!(contents))
  end

  def generate_modules(actors, secrets, output_path, seed \\ nil) do
    sequence = generate_sequence(actors, secrets, seed)
    real_actors = get_actors(sequence)
    first_message = Enum.fetch!(sequence.messages, 0)
    server_infos =
      for actor <- real_actors, into: %{} do
        info = generate_server_info(sequence, actor)
        info =
          if first_message.from == actor do
            %{info | first_message: first_message}
          else
            info
          end
        {actor, info}
      end

    for {name, _info} <- server_infos do
      container_path = Path.join(output_path, to_string(to_bare_name(name)))
      ebin_path = Path.join(container_path, "ebin")
      File.mkdir_p(ebin_path)
      write_single_app(server_infos, name, ebin_path)
      generate_dockerfile(name, container_path)
    end
    generate_compose(server_infos, output_path)

    :ok
  end
end
