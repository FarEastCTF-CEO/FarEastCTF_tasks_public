global _start
%include "vm.mac"

section .data
wrong db "NOPE", 10
OK db "RIGHT!", 10

prog1 dq retaddr
	branch entry
nonon:
	load_val rbx, 5
	load_val rax, wrong
	dq write
	Restore
kkk:
	load_val rbx, 7
	load_val rax, OK
	dq write
	Restore

strlen:
	place_imm_to_mem result_call, 0
	place_imm_to_mem local1, 0
	place_imm_to_mem local3, 10
    strlen_iter:
	take_byte_offset arg1, local1
	save_rax_to_mem local2
	compare_equal local2, result_call, local5
	branchZ local5, strlen_end
	compare_equal local2, local3, local5
	branchZ local5, strlen_end
	add_imm local1, 1, local1
	branch strlen_iter
   strlen_end:
	save_mem_mem result_call, local1
	Restore

entry:
	load_val r10, local_stor
        load_val r8, call_stack
	dq read
	load_val rax, input
	save_rax_to_mem arg1
	callFunc strlen
	place_imm_to_mem local1, 11
	compare_equal local1, result_call, local2
	branchZ local2, kk2
	branch fail
kk2:
	load_val rax, input
	dq dbg1
	dq deref
	load_val rbx, 0xffffffff
	dq and_rax_rbx
	save_reg_to_mem local1, rax
	place_imm_to_mem local6, 0xcafedead
	addvar local1, local6, local1
	place_imm_to_mem local2,0x1114f2dff
	compare_equal local1, local2, local3
	branchZ local3, kk3
	branch fail
kk3:
	load_val rbx, 4
	load_val rax, input
	dq add_rax_rbx
	dq deref
	load_val rbx, 0xffffffff
	dq and_rax_rbx
	save_reg_to_mem local1, rax
	addvar local1, local6, local1
	place_imm_to_mem local2, 0x10b421402
	compare_equal local1, local2, local3
	branchZ local3, kk4
	branch fail
kk4:
	load_val rbx,8
	load_val rax, input
	dq add_rax_rbx
	dq deref
	load_val rbx, 0xffffff
	dq and_rax_rbx
	save_reg_to_mem local1, rax
	addvar local1, local6, local1
	place_imm_to_mem local2, 0xcb431201
	compare_equal local1, local2, local3
	branchZ local3, succ	

fail:
	callFunc nonon
	dq exit
succ:
	callFunc kkk
	dq exit

section .bss
	call_stack resq 256
	local_stor resq 4096
	save_stack resq 1
        out_ptr resq 1
        result_call resq 1
	var1 resq 1
	var2 resq 1
	arg1 resq 1
	arg2 resq 1
	arg3 resq 1
	arg4 resq 1
	arg5 resq 1
	arg6 resq 1
	arg7 resq 1
	local1 resq 1
	local2 resq 1
	local3 resq 1
	local4 resq 1
	local5 resq 1
	local6 resq 1
	local7 resq 1
	local8 resq 1
	res1 resq 1
	res2 resq 1
	cmp_res resq 2
	input resb 256

section .text

copy_val:
        movsq
        ret


read:
	mov rax, 0
	mov rdi, 0
	mov rsi, input
	mov rdx, 256
	syscall
	ret

write:
	mov rsi, rax
	mov rdx, rbx
	mov rax, 1
	mov rdi, 1
	syscall
	ret 


exit:
	mov rax, 60
	syscall

dbg1:
	ret
dbg2:
	ret
dbg3:
	ret

pop_r10:
	pop r10
	ret
pop_r8:
	pop r8
	ret
mov_rax_r8:
	mov rax,r8
	ret

add_mem_imm_8:
	add qword [rax], 8
	ret

add_vars:
	mov rbx, [rbx]
	add [rax], rbx
	ret

add_mem_imm_4:
	add qword [rax], 4
	ret

mov_r9_rax:
	mov r9, rax
	ret

mov_rax_r9:
	mov rax, r9
	ret

add_rax_4:
	add rax,4
	ret
add_rax_8:
	add rax,8
	ret
add_rax_1:
	inc rax
	ret

get_eflags:
	lahf
	ret
mul_rax_rbx:
	mul rbx
	ret

xor_rax_rbx:
	xor rax, rbx
	ret

save_r8_mem:
	mov [r8], rax
	ret
take_r8_mem:
	mov rax, [r8]
	ret
add_rsp:
	add rsp, rax
	ret
change_stack:
	mov rsp, rax
	ret

take_r10_mem:
	mov rax, [r10]
	ret
save_r10_mem:
	mov [r10], rax
	ret

mov_r10_rax:
	mov r10, rax
	ret
mov_rax_r10:
	mov rax, r10
	ret
_start:
        savesreg
	mov [save_stack], rsp
	mov rsp, prog1
	ret
 finish:
 mov_r8_rax:
	mov r8, rax
	ret
 mov_r9_mem_byte:
	mov [r9], al
	ret
 mov_r9_mem_dword:
	mov [r9], eax
	ret
 mov_r9_mem:	
	mov [r9], rax
	ret
 pop_r12:
        pop r12
 retaddr:
	ret
 pop_rax:
	pop rax;
	ret
 mov_rbx_rax:
	mov rbx, rax
	ret 
 inc_r10:
	add r10, 8
	ret
 dec_r10:
	sub r10, 8
	ret
 save_rax_r12:
	mov [r12], rax
	ret
 mov_rax_rdi:
	mov rax, rdi
	ret
 extractZ:
	shr rax, 6
	and rax, 1
	xor rax, 1
	ret
 jpz:
	mov rdx, [cmp_res]
	cmp rdx, rbx
	jz mygin
	ret
  mygin:
	mov rsp, rax
	ret
	
 pop_rbx:
	pop rbx
	ret
 mov_rax_rsi:
	mov rax, rsi
	ret
 deref:
	mov rax, [rax]
	ret

 deref_dword:
	mov rax, [rax]
	mov rbx, 0xffffffff
	and rax, rbx
	ret
 mov_rax_rax:
        ret

 and_rax_rbx:
	and rax,rbx
	ret
 sub_rax_rbx:
	sub rax, rbx
	ret
 pop_rdi:
	pop rdi
	ret
 pop_rsi:
	pop rsi
	ret
 add_rax_rbx:
	add rax, rbx
	ret
 mov_r12data_rax:
	mov rax, [r12]
	ret
 mov_rax_rdx:
	mov rax, rdx
	ret

call_rax:
	call rax
	ret
