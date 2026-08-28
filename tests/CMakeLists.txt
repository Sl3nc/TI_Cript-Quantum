set(WORKLOAD_TESTS
    test_config
    test_kem
    test_dss
    test_sphincs
    test_rsa
    test_ecdsa
    test_ecdh
)

foreach(test_name IN LISTS WORKLOAD_TESTS)
    add_executable(${test_name} ${test_name}.c)
    target_link_libraries(${test_name} PRIVATE workloads)
    add_test(NAME ${test_name} COMMAND ${test_name})
endforeach()
